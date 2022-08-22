""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
import os


""" ===========================================================================
# >>> DATABASE
=========================================================================== """


class DataBase:
    URL = "postgresql://postgres:pass@database:5432/postgres"
    # URL = "postgresql://postgres:pass@localhost:5432/postgres"


""" ===========================================================================
# >>> MAIN CONFIG
=========================================================================== """


class MainConfig:
    INPUT_FILES_PATTERN = r"\w+?_(\d+).(\d+).(\d+)"
    UPLOAD_PATH = os.path.join("storage", "uploaded_files")
    TIME_FORMAT = "%H:%M:%S"
    DATE_FORMAT = "%Y.%m.%d"
    BASE_COORDINATES = {
        "Точка А": (55.882300, 37.725900),
        "Точка Б": (56.095498, 38.001631),
        "Точка С": (56.308696, 38.277362),
        "Точка Д": (56.521894, 38.553093),
        "Точка Е": (56.735093, 38.828825),
    }


""" ===========================================================================
# >>> SPARROW CONFIG
=========================================================================== """


class InfoConfig:
    INFO_NAME = "InfoLog"
    SELECT_STRING_LOG = "PARAMS [ip, a, b, c, d]"
    RE_TIMESTAMP = r"\d{2}:\d{2}:\d{2}"
    RE_VALUES = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}),(\d{1,3}\,\d{1,3}\,\d{1,3}\,\d{1,3})|(none)"
    RE_IP = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d{1,3})"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    COLUMN_NAMES = [
        "id_datetime",
        "ip",
        "a",
        "b",
        "c",
        "d",
        "e_absolute",
        "not_none",
        "f_percent",
        "e_percent"
    ]


""" ===========================================================================
# >>> COORDINATES CONFIG
=========================================================================== """


class CoordinatesConfig:
    COLOR_NAME = "ColoredCoordinate"
    TIME_NAME = "TimedCoordinate"
    COLUMN_NAMES = [
        "id_datetime",
        "longitude",
        "latitude",
        "height",
        "color"
    ]
