from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    none = "none"
    uploaded = "uploaded"
    processed = "processed"


class ReportBase(BaseModel):
    id_date: date
    info_log: Status
    timed_coordinates: Status
    colored_coordinates: Status

    class Config:
        orm_mode = True

class ReportUpdate(BaseModel):
    id_date: date
    info_log: Status | None = None
    timed_coordinates: Status | None = None
    colored_coordinates: Status | None = None

    class Config:
        orm_mode = True


class InfoBase(BaseModel):
    id_datetime: datetime
    ip: str
    a: str
    b: str
    c: str
    d: str
    e_absolute: str
    f_percent: int
    e_percent: int

    class Config:
        orm_mode = True


class CoordinatesBase(BaseModel):
    id_datetime: datetime
    latitude: float
    longitude: float
    height: int
    color: str

    class Config:
        orm_mode = True
