""" ===========================================================================
# >>> IMPORTS
=========================================================================== """
import re
from datetime import date, datetime
from operator import __lt__
from typing import Iterable

import pandas as pd
from config import InfoConfig as ic


""" ===========================================================================
# >>> INFO LOG PARSER
=========================================================================== """


class InfoLogParser:
    def __init__(self, file_path: str, date: date) -> None:
        self.file_path = file_path
        self.date = date
        self.dataframe: pd.DataFrame | None = None

    def filter_dataframe(self) -> None:
        indexes = self.dataframe.index[self.dataframe["not_none"] == True]

        if indexes.empty:
            self.dataframe = self.dataframe.drop("not_none", axis=1)
            return

        first = indexes[0]
        last = indexes[-1]

        if first > 100:
            first -= 100
        else:
            first = 0

        if self.dataframe.shape[0] - last > 100:
            last += 100
        else:
            last = self.dataframe.shape[0] - 1

        filtered_df = self.dataframe[
            self.dataframe.index.isin(range(first, last))
        ]

        self.dataframe = filtered_df.drop("not_none", axis=1)

    def data_gathering(self) -> None:
        list_df = []

        with open(self.file_path, "r") as info_file:
            for line in info_file:
                if ic.SELECT_STRING_LOG in line:

                    # Search fot Time in log string
                    time = re.search(ic.RE_TIMESTAMP, line).group(0)

                    # Create DateTime stamp (datetime format) from date and time
                    timestamp = datetime.strptime(
                        f"{self.date} {time}", ic.DATETIME_FORMAT
                    )

                    # Extract all Values and according IPs if exists, also none values
                    values = re.findall(ic.RE_VALUES, line)

                    # Convert values to int and skip all the none
                    df_values = [[] for i in range(6)]
                    for value in values:
                        if value[0] != '':
                            tmp = tuple(map(int, value[1].split(",")))
                            df_values[0].append(value[0])
                            for i in range(len(tmp)):
                                df_values[i+1].append(tmp[i])
                        else:
                            for i in range(5):
                                df_values[i].append(None)

                    # Add all parsed values to resulting list
                    for i in range(len(df_values[0])):

                        if df_values[0][i] is not None:

                            e_absolute = df_values[1][i]
                            if df_values[2][i] < 110:
                                e_absolute += 110 - df_values[2][i]

                            df_values[5].append(e_absolute)
                        else:
                            df_values[5].append(None)
                        
                    list_df.append([timestamp, *df_values, any(df_values[5])])

        # Create DataFrame from parsed strings
        df = pd.DataFrame(list_df, columns=ic.COLUMN_NAMES[:-2])
        self.dataframe = df

        print(df.shape)

        # Filter data to remoove unneccesary info
        self.filter_dataframe()

     
    def analize_data(self) -> None:
        self.dataframe[ic.COLUMN_NAMES[-2]] = \
            self.dataframe["a"].apply(self.analize)

     
    def analize_rcv(self) -> None:
        self.dataframe[ic.COLUMN_NAMES[-1]] = \
            self.dataframe["e_absolute"].apply(self.analize)

     
    def parse(self) -> pd.DataFrame | None:
        self.data_gathering()
        self.analize_data()
        self.analize_rcv()

        # If all values equals 100 - empty log
        if self.dataframe[ic.COLUMN_NAMES[-1]].nunique == 1:
            return pd.DataFrame()

        self.dataframe[ic.COLUMN_NAMES[1]] = \
            self.dataframe[ic.COLUMN_NAMES[1]].apply(self.replace_ip)
        
        for col in ic.COLUMN_NAMES[2:-3]:
            self.dataframe[col] = \
                self.dataframe[col].apply(lambda x: list(map(str, x)))\
                    .str.join("\n").apply(str.replace, args=("None", "-"))

        self.dataframe[ic.COLUMN_NAMES[1:-3]] = \
            self.dataframe[ic.COLUMN_NAMES[1:-3]].astype("string")

        return self.dataframe

    # Utilities ===============================================================
    @staticmethod
    def replace_ip(lst: list) -> list:
        res = list(map(str, lst))
        for i in range(len(res)):
            if short_ip := re.search(ic.RE_IP, res[i]):
                res[i] = short_ip.group(1)
            else:
                res[i] = "-"
        return "\n".join(res)

    # Analizing ===============================================================

    @staticmethod
    def check_none(elem: Iterable[int]) -> bool:
        for el in elem:
            if el is not None:
                return True
        return False

    @staticmethod
    def check_one(elem: Iterable[int], val: int) -> bool:
        for el in elem:
            if el is not None:
                if el <= val:
                    return True
        return False

    @staticmethod
    def check_two(elem: Iterable[int], val: int) -> bool:
        cnt = 0
        for el in elem:
            if el is not None:
                if el <= val:
                    cnt += 1
        if cnt >= 2:
            return True
        else:
            return False

    @staticmethod
    def check_min(elem: Iterable[int], max_val: int) -> float:
        min_val = max_val
        for el in elem:
            if el is not None:
                if min_val > el:
                    min_val = el
        return min_val / max_val

    def analize(self, elem: Iterable[int]) -> int:
        if self.check_none(elem):
            if self.check_one(elem, 3):
                return 0
            if self.check_two(elem, 20):
                return 0
            return int(self.check_min(elem, 110) * 100)
        else:
            return 100
