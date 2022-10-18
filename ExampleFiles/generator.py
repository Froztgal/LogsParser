""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
import os
from datetime import date, datetime, timedelta
from random import choice, randint
from string import ascii_letters, digits

from templates import (info_log_template, info_log_values_template,
                       placemark_template, point_template,
                       styled_coordinate_kml_template,
                       timed_coordinate_kml_template)

""" ===========================================================================
# >>> SETTINGS
=========================================================================== """
FILES_PATH = "ExampleFiles/Files"

INFO_LOG_FILENAME = "InfoLog"
TIMED_COORDINATE_KML_FILENAME = "TimedCoordinate"
STYLED_COORDINATE_KML_FILENAME = "ColoredCoordinate"

LOG_STATES = ["INFO", "DEBUG", "WARNING", "ERROR"]

START_POINT = (55.8823, 37.7259)
STOP_POINT = (56.735093, 38.828825)

STYLE_IDS = ("bad", "normal", "good")


""" ===========================================================================
# >>> FUNCTIONS
=========================================================================== """


def get_random_string() -> str:
    state = choice(LOG_STATES)
    message = "".join(choice(ascii_letters + digits)
                      for _ in range(randint(1, 100)))
    return f"{state}: {message}\n"


def get_random_ip() -> str:
    return ".".join(map(str, (randint(0, 255) for _ in range(4))))


def generate_info_log(log_date: date) -> None:
    file_path = os.path.join(FILES_PATH, f"{INFO_LOG_FILENAME}_{log_date}")
    row_number = randint(100, 1000)
    times = ((datetime.now() + timedelta(seconds=i)).strftime("%H:%M:%S")
             for i in range(row_number))
    with open(file_path, "w") as info_log:
        for time in times:
            if randint(0, 100) > 75:
                info_log.write(get_random_string())
            else:
                values = []
                for _ in range(3):
                    values_mapper = {
                        "ip": get_random_ip(),
                        "a": randint(0, 120),
                        "b": randint(0, 120),
                        "c": randint(0, 20),
                        "d": randint(0, 120)
                    }
                    values.append(
                        info_log_values_template.substitute(values_mapper))
                template_mapper = {
                    "time": time,
                    "values_1": values[0],
                    "values_2": values[1],
                    "values_3": values[2]
                }
                info_log.write(info_log_template.substitute(template_mapper))


def generate_timed_coordinate_kml(log_date: date) -> None:
    file_path = os.path.join(
        FILES_PATH, f"{TIMED_COORDINATE_KML_FILENAME}_{log_date}")
    row_number = 100
    times = ((datetime.now() + timedelta(seconds=i))
             .strftime("%y-%m-%dT%H:%M:%SZ") for i in range(row_number))
    steps = (
        (STOP_POINT[0] - START_POINT[0]) / row_number,
        (STOP_POINT[1] - START_POINT[1]) / row_number
    )
    coords = ((START_POINT[0] + steps[0] * i, START_POINT[1] + steps[1] * i)
              for i in range(row_number))
    with open(file_path, "w") as timed_coords:
        values = ""
        for time in times:
            coord = next(coords)
            value = point_template.substitute(
                {
                    "datetimez": time,
                    "longitude": coord[1],
                    "latitude": coord[0],
                    "height": randint(80, 200)
                }
            )
            values += value

        timed_coords.write(
            timed_coordinate_kml_template.substitute({"points": values}))


def generate_styled_coordinate_kml(log_date: date) -> None:
    file_path = os.path.join(
        FILES_PATH, f"{STYLED_COORDINATE_KML_FILENAME}_{log_date}")
    row_number = 100
    steps = (
        (STOP_POINT[0] - START_POINT[0]) / row_number,
        (STOP_POINT[1] - START_POINT[1]) / row_number
    )
    coords = ((START_POINT[0] + steps[0] * i, START_POINT[1] + steps[1] * i, i)
              for i in range(row_number))
    with open(file_path, "w") as styled_coords:
        values = ""
        for coord in coords:
            value = placemark_template.substitute(
                {
                    "id": coord[2],
                    "color": choice(STYLE_IDS),
                    "longitude": coord[1],
                    "latitude": coord[0],
                    "height": randint(80, 200)
                }
            )
            values += value

        styled_coords.write(
            styled_coordinate_kml_template.substitute({"placemarks": values}))

""" ===========================================================================
# >>> MAIN
=========================================================================== """
if __name__ == "__main__":
    # Generate info_logs
    log_date = date.today() + timedelta(days=0)
    generate_info_log(log_date)
    # Generate timed_coordinates
    log_date = date.today() + timedelta(days=0)
    generate_timed_coordinate_kml(log_date)
    # Generate styled_coordinates
    log_date = date.today() + timedelta(days=0)
    generate_styled_coordinate_kml(log_date)
