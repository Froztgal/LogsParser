from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Report(Base):
    __tablename__ = "reports"

    id_date = Column(Date, primary_key=True, index=True)
    info_log = Column(String)
    timed_coordinates = Column(String)
    colored_coordinates = Column(String)


class Info(Base):
    __tablename__ = "info"

    id_datetime = Column(DateTime, primary_key=True, index=True)
    ip = Column(String)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    e_absolute = Column(String)
    f_percent = Column(Integer)
    e_percent = Column(Integer)


class Coordinates(Base):
    __tablename__ = "coordinates"

    id_datetime = Column(DateTime, primary_key=True, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    height = Column(Integer)
    color = Column(String)
