""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
from datetime import date

import storage.database.crud as crud
import storage.database.models as models
import storage.database.schemas as schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from storage.database.database import SessionLocal, engine

""" ===========================================================================
# >>> INITIALIZING
=========================================================================== """
models.Base.metadata.create_all(bind=engine)

database_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" ===========================================================================
# >>> REPORTS
=========================================================================== """


# GET =========================================================================
@database_router.get("/reports/get_all/",
                     response_model=list[schemas.ReportBase],
                     tags=["DataBase/Reports"])
async def reports_get_all(db: Session = Depends(get_db)):
    reports = crud.get_reports(db)
    return reports


@database_router.get("/reports/get/{date}",
                     response_model=schemas.ReportBase,
                     tags=["DataBase/Reports"])
async def reports_get(date: date, db: Session = Depends(get_db)):
    report = crud.get_report(db, date)
    return report


# POST ========================================================================
@database_router.post("/reports/create/",
                      response_model=schemas.ReportBase,
                      tags=["DataBase/Reports"])
async def report_create(report: schemas.ReportBase,
                        db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report.id_date)
    if db_report:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Report for this date already exists!")
    return crud.create_report(db, report)


# UPDATE ======================================================================
@database_router.put("/reports/update/",
                     tags=["DataBase/Reports"])
async def reports_update(updater: schemas.ReportUpdate,
                         db: Session = Depends(get_db)):
    updated = crud.update_report(db, updater)
    return JSONResponse(content={"Number of updated rows": updated})


# DELETE ======================================================================
@database_router.delete("/reports/delete/{date}",
                        tags=["DataBase/Reports"])
async def reports_update(date: date, db: Session = Depends(get_db)):
    deleted = crud.delete_report(db, date)
    return JSONResponse(content={"Number of deleted rows": deleted})

""" ===========================================================================
# >>> INFO
=========================================================================== """


# GET =========================================================================
@database_router.get("/info/get_len/{date}",
                     tags=["DataBase/Info"])
async def info_get_all(date: date, db: Session = Depends(get_db)):
    length = crud.get_info_len(db, date)
    return JSONResponse(content={"Number of rows": length})


@database_router.get("/info/get_on_date/{date}",
                     tags=["DataBase/Info"])
async def info_get_on_date(date: date,
                           offset: int | None = None,
                           limit: int | None = None,
                           db: Session = Depends(get_db)):
    info = crud.get_info_on_date(db, date, offset, limit)
    return info


@database_router.get("/info/get_data_on_date/{date}",
                     tags=["DataBase/Info"])
async def info_get_f_percent_on_date(date: date, offset: int, limit: int,
                                     db: Session = Depends(get_db)):
    data = crud.get_f_percent_on_date(db, date, offset, limit)
    return {d["id_datetime"]: d["f_percent"] for d in data}


@database_router.get("/info/get_rcv_on_date/{date}",
                     tags=["DataBase/Info"])
async def info_get_e_percent_on_date(date: date, db: Session = Depends(get_db)):
    e_percent = crud.get_e_percent_on_date(db, date)
    return e_percent


# POST ========================================================================
@database_router.post("/info/create_on_date/{date}",
                      tags=["DataBase/Info"])
async def info_create_on_date(date: date,
                              info: list[schemas.InfoBase],
                              db: Session = Depends(get_db)):
    db_info = crud.get_info_on_date(db, date, 0, 1)
    if db_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="InfoLog for this date already exists!")
    num = crud.create_info(db, info)
    return JSONResponse(content={"Number of inserted rows": num})


# DELETE ======================================================================
@database_router.delete("/info/delete_on_date/{date}",
                        tags=["DataBase/Info"])
async def info_delete_on_date(date: date, db: Session = Depends(get_db)):
    deleted = crud.delete_info(db, date)
    return JSONResponse(content={"Number of deleted rows": deleted})


""" ===========================================================================
# >>> COORDINATES
=========================================================================== """


# GET =========================================================================
@database_router.get("/coordinates/get_all/",
                     response_model=list[schemas.CoordinatesBase],
                     tags=["DataBase/Coordinates"])
async def coordinates_get_all(db: Session = Depends(get_db)):
    coordinates = crud.get_coordinates(db)
    return coordinates


@database_router.get("/coordinates/get_on_date/{date}",
                     response_model=list[schemas.CoordinatesBase],
                     tags=["DataBase/Coordinates"])
async def coordinates_get_on_date(date: date, db: Session = Depends(get_db)):
    coordinates = crud.get_coordinates_on_date(db, date)
    return coordinates


# POST ========================================================================
@database_router.post("/coordinates/create_on_date/{date}",
                      response_model=list[schemas.CoordinatesBase],
                      tags=["DataBase/Coordinates"])
async def coordinates_create_on_date(date: date,
                                     coordinates: list[schemas.CoordinatesBase],
                                     db: Session = Depends(get_db)):
    db_info = crud.get_coordinates_on_date(db, date=date)
    if db_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Coordinates for this date already exists!")
    return crud.create_coordinates(db, coordinates)


# DELETE ======================================================================
@database_router.delete("/coordinates/delete_on_date/{date}",
                        tags=["DataBase/Coordinates"])
async def coordinates_delete_on_date(date: date, db: Session = Depends(get_db)):
    deleted = crud.delete_coordinates(db, date)
    return JSONResponse(content={"Number of deleted rows": deleted})


""" ===========================================================================
# >>> INFO + COORDINATES
=========================================================================== """


# GET =========================================================================
@database_router.get("/slc/get_on_date/{date}", tags=["DataBase/SLC"])
async def slc_get_on_date(date: date,
                          offset: int | None = None,
                          limit: int | None = None,
                          db: Session = Depends(get_db)):
    slc = crud.get_ilc_on_date(db, date, offset, limit)
    return slc
