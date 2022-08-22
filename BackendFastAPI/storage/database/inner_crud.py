""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
from datetime import date, datetime, time

import pandas as pd
import storage.database.models as models
import storage.database.schemas as schemas
from numpy import float64
from sqlalchemy import TIME, case, func
from storage.database.database import SessionLocal, engine

""" ===========================================================================
# >>> INFO
=========================================================================== """


def create_info_df(info: pd.DataFrame):
    info.to_sql("info", con=engine, if_exists='append', index=False)
    return len(info)


""" ===========================================================================
# >>> COORDINATES
=========================================================================== """


def create_coordinates_df(coordinates: pd.DataFrame):
    coordinates.to_sql("coordinates", con=engine,
                       if_exists='append', index=False)
    return len(coordinates)


def find_nearest(coordinates: tuple[float64, float64],
                 date: date) -> tuple[datetime, float64]:
    with SessionLocal() as db:
        return db.query(
            models.Coordinates.id_datetime,
            func.sqrt(
                func.pow(models.Coordinates.latitude - coordinates[0], 2) +
                func.pow(models.Coordinates.longitude - coordinates[1], 2)
            ).label('test')
        ).filter(func.DATE(models.Coordinates.id_datetime) == date)\
            .order_by('test').first()


""" ===========================================================================
# >>> REPORTS
=========================================================================== """


def get_report(date: date):
    with SessionLocal() as db:
        return db.query(models.Report).\
            filter(models.Report.id_date == date).first()


def create_report(report: schemas.ReportBase):
    with SessionLocal() as db:
        report = models.Report(**report.dict())
        db.add(report)
        db.commit()
    return report


def update_report(updater: schemas.ReportUpdate):
    with SessionLocal() as db:
        updated_report = db.query(models.Report).\
            filter(models.Report.id_date == updater.id_date).\
            update(updater.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    return updated_report


""" ===========================================================================
# >>> FILES
=========================================================================== """


def get_errors(date: date, start: time, end: time):
    with SessionLocal() as db:
        return db.query(
            models.Info.id_datetime,
            models.Info.e_percent).\
            filter(
                func.DATE(models.Info.id_datetime) == date,
                models.Info.id_datetime.cast(TIME) >= start,
                models.Info.id_datetime.cast(TIME) <= end).\
            all()


def get_plot(date: date):
    with SessionLocal() as db:
        return db.query(models.Info.id_datetime,
                        models.Info.e_percent).\
            filter(func.DATE(models.Info.id_datetime) == date).\
            order_by(models.Info.id_datetime).all()


def get_kml_merged(date: date):
    with SessionLocal() as db:
        return db.query(models.Coordinates.latitude,
                        models.Coordinates.longitude,
                        models.Coordinates.height,
                        case(
                            (models.Info.e_percent <= 10, 'good'),
                            (models.Info.e_percent <= 50, 'normal'),
                            else_='bad'
                        ).label("color")
                        ).\
            select_from(models.Coordinates).\
            join(models.Info,
                 models.Coordinates.id_datetime == models.Info.id_datetime).\
            filter(func.DATE(models.Coordinates.id_datetime) == date).all()
