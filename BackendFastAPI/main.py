""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
import logging
import os
import re
import tempfile
from datetime import date, datetime, time

import pandas as pd
import plotly.graph_objs as go
from fastapi import FastAPI, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError

from config import CoordinatesConfig as cc
from config import InfoConfig as ic
from config import MainConfig as mc
from storage.database import inner_crud, schemas
from storage.database.main import database_router
from templates.kml import kml_template, placemark
from utils.coordinates_parser import CoordinateParser
from utils.info_log_parser import InfoLogParser

""" ===========================================================================
# >>> INITIALIZING
=========================================================================== """

app = FastAPI()
app.include_router(database_router, prefix="/database")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)


""" ===========================================================================
# >>> APP
=========================================================================== """


@app.post("/upload_files/", status_code=status.HTTP_201_CREATED, tags=["App"])
async def create_upload_files(files: list[UploadFile]):

    saved = []
    not_saved = []

    # Save all files matching pattern
    for file in files:

        # Filter the files
        if date := re.findall(mc.INPUT_FILES_PATTERN, file.filename):
            date = date[0]
            str_date = '-'.join(date)

            # Create folder if not exist
            upload_path = os.path.join(mc.UPLOAD_PATH, str_date)
            if not os.path.exists(upload_path):
                logging.info(os.getcwd())
                os.makedirs(upload_path)

            # Create record in DB for this date
            if not inner_crud.get_report(str_date):
                inner_crud.create_report(
                    schemas.ReportBase(id_date=str_date,
                                       info_log="none",
                                       timed_coordinates="none",
                                       colored_coordinates="none")
                )

            saved.append(file.filename)

            # Change name of the file and update status to "Uploaded" in DB
            if ic.INFO_NAME in file.filename:
                new_filename = f"{ic.INFO_NAME}"
                inner_crud.update_report(
                    schemas.ReportUpdate(id_date=str_date,
                                         info_log="uploaded")
                )
            elif cc.COLOR_NAME in file.filename:
                new_filename = f"{cc.COLOR_NAME}"
                inner_crud.update_report(
                    schemas.ReportUpdate(id_date=str_date,
                                         colored_coordinates="uploaded")
                )
            elif cc.TIME_NAME in file.filename:
                new_filename = f"{cc.TIME_NAME}"
                inner_crud.update_report(
                    schemas.ReportUpdate(id_date=str_date,
                                         timed_coordinates="uploaded")
                )

            # Read the file
            contents = await file.read()

            # Save the file
            with open(os.path.join(upload_path, new_filename), "wb") as log:
                log.write(contents)

        else:
            not_saved.append(file.filename)

    return {
        "Saved files": saved,
        "Not saved files": not_saved
    }


def clean(file_path: str) -> None:
    os.remove(file_path)
    path = os.path.split(file_path)[0]
    if os.listdir(path) == 0:
        os.rmdir(path)


@app.post("/process_info/{date}", status_code=status.HTTP_201_CREATED,
          tags=["App"])
async def process_info(date: date):

    file_path = os.path.join(mc.UPLOAD_PATH, str(date), ic.INFO_NAME)

    # Check that file uploaded
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "Warning":
                "InfoLog for this date not uploaded, please upload it and try again."
            }
        )

    # Parse the log file
    parser = InfoLogParser(
        file_path=file_path,
        date=date
    )
    parsed = parser.parse()

    if parsed.empty:
        return JSONResponse(
            content={
                "Warning":
                "InfoLog has no useful data, please remove this report."
            }
        )

    try:
        inner_crud.create_info_df(parsed)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="InfoLog for this date already exists!")

    clean(file_path)

    # Change status to "Processed" in DB
    inner_crud.update_report(
        schemas.ReportUpdate(id_date=date, info_log="processed")
    )

    return JSONResponse(content={"Number of parsed rows": len(parsed)})


@app.post("/process_coordinates/{date}", status_code=status.HTTP_201_CREATED,
          tags=["App"])
async def process_coordinates(date: date):

    # Path of files
    time_path = os.path.join(mc.UPLOAD_PATH, str(date), cc.TIME_NAME)
    color_path = os.path.join(mc.UPLOAD_PATH, str(date), cc.COLOR_NAME)

    # Chek both file exists
    if not os.path.exists(time_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You don't upload time file!")

    if not os.path.exists(color_path):
        color_path = None
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail="You don't upload color file!")

    parser = CoordinateParser(time_path, color_path)
    parsed = parser.parse()
    print(parsed["id_datetime"].nunique())

    try:
        inner_crud.create_coordinates_df(parsed)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Coordinates for this date already exists!")

    clean(time_path)

    # Change status to "Processed" in DB
    if color_path:
        clean(color_path)
        inner_crud.update_report(
            schemas.ReportUpdate(id_date=date, colored_coordinates="processed",
                                 timed_coordinates="processed")
        )
    else:
        inner_crud.update_report(
            schemas.ReportUpdate(id_date=date, timed_coordinates="processed")
        )

    return JSONResponse(content={"Number of parsed rows": len(parsed)})


@app.get("/dashboard/download_errors/{date}", status_code=status.HTTP_200_OK,
         tags=["App"])
async def get_file(date: date, start: time, end: time):
    errors = inner_crud.get_errors(date, start, end)

    if not errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You don't upload InfoLog file!")

    with tempfile.NamedTemporaryFile("w", delete=False) as file:
        for row in errors:
            file.write(f"{row[0].strftime(mc.TIME_FORMAT)} {row[1]}\n")
        return FileResponse(
            path=file.name,
            filename=f"errors_{date.strftime(mc.DATE_FORMAT)}.txt"
        )


def colorize(value):
    if value <= 10:
        return -1
    elif value <= 50:
        return 0
    else:
        return 1


@app.post("/dashboard/download_plot/{date}", status_code=status.HTTP_200_OK,
          tags=["App"])
async def get_plot(date: date, data: dict):
    plot_data = inner_crud.get_plot(date)

    if not plot_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You don't upload InfoLog file!")

    plot_df = pd.DataFrame(plot_data)
    plot_df["color"] = plot_df["e_percent"].apply(colorize)

    colorscale = [
        [0, 'rgb(84, 156, 73)'],
        [0.5, 'rgb(255, 215, 0)'],
        [1.0, 'rgba(255, 49, 62, 0.9)']
    ]

    fig = go.Figure(
        # layout={'plot_bgcolor': 'rgba(0,0,0,0)'}
    )
    fig.add_trace(
        go.Scatter(
            x=plot_df['id_datetime'],
            y=plot_df['e_percent'],
            mode='lines+markers',
            marker={
                'color': plot_df["color"],
                'colorscale': colorscale,
                'size': 4,
            },
            line={
                'color': 'rgba(68, 68, 68, 0.3)',
                'width': 1
            }
        )
    )

    for k, v in data["timestamps"].items():
        # Convert to timestamp and move to UTC timezone from Moscow
        timestamp = datetime.strptime(f"{date} {v}", "%Y-%m-%d %H:%M")
        fig.add_vline(
            # x=timestamp.timestamp() * 1000 + 3 * 3600,
            x=(timestamp.timestamp() - 3 * 3600) * 1000,
            line_width=3,
            line_dash="dash",
            annotation_text=k,
            annotation_position="top",
            annotation_textangle=-30
        )

    with tempfile.NamedTemporaryFile("wb", delete=False) as file:
        fig.write_html(file.name)
        return FileResponse(
            path=file.name,
            filename=f"analize_{date.strftime(mc.DATE_FORMAT)}.html"
        )


@app.get("/dashboard/get_base_time/{date}", status_code=status.HTTP_200_OK,
         tags=["App"])
async def get_base_time(date: date):
    result = {}
    for k, v in mc.BASE_COORDINATES.items():
        time = inner_crud.find_nearest(v, date)
        if time:
            result[k] = time[0].strftime("%H:%M")
        else:
            result[k] = "00:00"
    return JSONResponse(result)


@app.get("/dashboard/get_kml/{date}", status_code=status.HTTP_200_OK,
         tags=["App"])
async def get_kml(date: date):
    kml_data = inner_crud.get_kml_merged(date)

    if not kml_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't upload InfoLog OR Coordinates files!")

    places = ""
    for id in range(len(kml_data)):
        place = placemark.substitute(id=id, **kml_data[id])
        places += place

    with tempfile.NamedTemporaryFile("w", delete=False) as file:
        file.write(kml_template.substitute(placemarks=places))
        return FileResponse(
            path=file.name,
            filename=f"map_{date.strftime(mc.DATE_FORMAT)}.kml"
        )


@ app.get("/", status_code=status.HTTP_200_OK)
async def redirect_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
