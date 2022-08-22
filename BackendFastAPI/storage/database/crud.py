""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
from datetime import date

import storage.database.models as models
import storage.database.schemas as schemas
from sqlalchemy import case, func
from sqlalchemy.orm import Session

""" ===========================================================================
# >>> REPORTS
=========================================================================== """


# GET =========================================================================
def get_reports(db: Session):
    return db.query(models.Report).order_by(models.Report.id_date.desc()).all()


def get_report(db: Session, date: date):
    return db.query(models.Report).\
        filter(models.Report.id_date == date).first()


# POST ========================================================================
def create_report(db: Session, report: schemas.ReportBase):
    report = models.Report(**report.dict())
    db.add(report)
    db.commit()
    return report


# UPDATE ======================================================================
def update_report(db: Session, updater: schemas.ReportUpdate):
    num_updated = db.query(models.Report).\
        filter(models.Report.id_date == updater.id_date).\
        update(updater.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return num_updated


# DELETE ======================================================================
def delete_report(db: Session, date: date):
    num_deleted = db.query(models.Report).\
        filter(models.Report.id_date == date).delete(synchronize_session=False)
    db.commit()
    return num_deleted


""" ===========================================================================
# >>> INFO
=========================================================================== """


# GET =========================================================================
def get_info_len(db: Session, date: date):
    return db.query(models.Info).\
        filter(func.DATE(models.Info.id_datetime) == date).count()


def get_info_on_date(db: Session,
                        date: date,
                        offset: int | None = None,
                        limit: int | None = None):
    return db.query(
        func.to_char(models.Info.id_datetime, 'HH24:MI:SS')
            .label("id_datetime"),
        models.Info.ip,
        models.Info.a,
        models.Info.b,
        models.Info.c,
        models.Info.d,
        models.Info.e_absolute,
        models.Info.f_percent,
        models.Info.e_percent,
        case(
            (models.Info.e_percent <= 10, 'good'),
            (models.Info.e_percent <= 50, 'normal'),
            else_='bad'
        ).label("color")
    ).filter(func.DATE(models.Info.id_datetime) == date)\
        .offset(offset).limit(limit).all()


def get_f_percent_on_date(db: Session, date: date, skip: int, limit: int):
    return db.query(models.Info.id_datetime, models.Info.f_percent).\
        filter(func.DATE(models.Info.id_datetime) == date).\
        offset(skip).limit(limit).all()


def get_e_percent_on_date(db: Session, date: date):
    return db.query(models.Info.id_datetime, models.Info.e_percent).\
        filter(func.DATE(models.Info.id_datetime) == date).all()


# POST ========================================================================
def create_info(db: Session, info: list[schemas.InfoBase]):
    dict_objects = map(dict, info)
    db.bulk_insert_mappings(models.Info, dict_objects)
    db.commit()
    return len(info)


# DELETE ======================================================================
def delete_info(db: Session, date: date):
    num_deleted = db.query(models.Info).\
        filter(func.DATE(models.Info.id_datetime) == date).\
        delete(synchronize_session=False)
    db.commit()
    return num_deleted


""" ===========================================================================
# >>> COORDINATES
=========================================================================== """


# GET =========================================================================
def get_coordinates(db: Session):
    return db.query(models.Coordinates).all()


def get_coordinates_on_date(db: Session, date: date):
    return db.query(models.Coordinates).\
        filter(func.DATE(models.Coordinates.id_datetime) == date).all()


# POST ========================================================================
def create_coordinates(db: Session, coordinates: list[schemas.CoordinatesBase]):
    dict_objects = map(dict, coordinates)
    db.bulk_insert_mappings(models.Coordinates, dict_objects)
    db.commit()
    return coordinates


# DELETE ======================================================================
def delete_coordinates(db: Session, date: date):
    num_deleted = db.query(models.Coordinates).\
        filter(func.DATE(models.Coordinates.id_datetime) == date).\
        delete(synchronize_session=False)
    db.commit()
    return num_deleted


""" ===========================================================================
# >>> INFO + COORDINATES
=========================================================================== """


# GET =========================================================================
def get_ilc_on_date(db: Session,
                    date: date,
                    offset: int | None = None,
                    limit: int | None = None):
    return db.query(
        func.to_char(models.Coordinates.id_datetime, 'HH24:MI:SS')
            .label("id_datetime"),
        models.Coordinates.latitude,
        models.Coordinates.longitude,
        models.Coordinates.height,
        models.Coordinates.color,
        models.Info.ip,
        models.Info.a,
        models.Info.b,
        models.Info.c,
        models.Info.d,
        models.Info.e_absolute,
        models.Info.f_percent,
        models.Info.e_percent
    ).select_from(models.Coordinates)\
        .join(models.Info,
              models.Coordinates.id_datetime == models.Info.id_datetime,
              isouter=True)\
        .filter(func.DATE(models.Coordinates.id_datetime) == date)\
        .offset(offset).limit(limit).all()
