""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
import io
from datetime import timedelta
from xml.dom import minidom

import pandas as pd
from config import CoordinatesConfig as cc


""" ===========================================================================
# >>> COORDINATES PARSER
=========================================================================== """


class CoordinateParser:

    def __init__(self, time_path: str, color_path: str | None = None) -> None:
        self.time_path = time_path
        self.color_path = color_path
        self.time_df: pd.DataFrame | None = None
        self.color_df: pd.DataFrame | None = None

    def get_time_coord(self) -> None:
        doc = minidom.parse(self.time_path)
        traks = doc.getElementsByTagName("gx:Track")[0]

        tmp_file = io.StringIO()
        tmp_file.write(f"{','.join(cc.COLUMN_NAMES[:-1])}\n")
        for child in traks.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.tagName == "when":
                    tmp_file.write(child.firstChild.data + ",")
                if child.tagName == "gx:coord":
                    coords = map(float, child.firstChild.data.split(" "))
                    coords = ["{:2.4f}".format(i) for i in coords]
                    tmp_file.write(",".join(coords) + "\n")

        tmp_file.seek(0)
        self.time_df = pd.read_csv(tmp_file)
        tmp_file.close()

        self.time_df[cc.COLUMN_NAMES[-2]] = \
            self.time_df[cc.COLUMN_NAMES[-2]].apply(int)

        self.time_df[cc.COLUMN_NAMES[0]] = \
            self.time_df[cc.COLUMN_NAMES[0]].apply(pd.to_datetime)

    def get_color_coord(self) -> None:

        doc = minidom.parse(self.color_path)

        marks = doc.getElementsByTagName("Placemark")
        marks_list = []

        for child in marks:
            coord_style = child.getElementsByTagName(
                "styleUrl")[0].firstChild.data[1:]
            coords = child.getElementsByTagName(
                "coordinates")[0].firstChild.data
            coords = list(map(float, coords.split(",")))[:-1]
            marks_list.append((*coords, coord_style))

        self.color_df = pd.DataFrame.from_records(
            marks_list, columns=[*cc.COLUMN_NAMES[1:3], cc.COLUMN_NAMES[-1]])

        self.color_df[cc.COLUMN_NAMES[1:-2]] = \
            self.color_df[cc.COLUMN_NAMES[1:-2]].apply(round, args=(4,))

    def parse(self) -> None:
        # Proccess files
        if self.time_path and self.color_path:
            self.get_time_coord()
            self.get_color_coord()

            # Merge
            coordinates_df = self.time_df.merge(
                self.color_df, on=cc.COLUMN_NAMES[1:3])

        else:
            self.get_time_coord()
            coordinates_df = self.time_df
            coordinates_df[cc.COLUMN_NAMES[-1]] = None

        # Conver to Moscow datetime
        # coordinates_df["id_datetime"] = \
        #     coordinates_df["id_datetime"] + timedelta(hours=3)

        return coordinates_df.drop_duplicates()
