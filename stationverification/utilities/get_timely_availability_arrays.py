import arrow

from datetime import date
import pandas as pd
from pandas.core.frame import DataFrame
from typing import Any, List, Tuple


def get_timely_availability_arrays(
    latencies: DataFrame, threshold: float
) -> Tuple[Any, Any, Any, Any]:
    list_of_HNN_timely_availability_dictionaries: List[dict] = []
    list_of_HNZ_timely_availability_dictionaries: List[dict] = []
    list_of_HNE_timely_availability_dictionaries: List[dict] = []

    timely_availability_percentage_array_days_axis: List[date] = []
    for latency_dataframe in latencies:
        if not latency_dataframe.empty:
            current_HNN_dictionary = {}
            HNN_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNN"]
            total_number_of_HNN_latencies = HNN_latencies["data_latency"].size

            number_of_HNN_latencies_below_threshold = HNN_latencies.loc[(
                HNN_latencies["data_latency"] <= threshold) &
                (HNN_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNN_latencies_above_threshold = HNN_latencies.loc[(
                HNN_latencies["data_latency"] > threshold) &
                (HNN_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNN_latencies_that_are_negative = HNN_latencies.loc[
                HNN_latencies["data_latency"] == -1]["data_latency"].size

            if total_number_of_HNN_latencies == 0:
                current_HNN_dictionary = \
                    {'below_threshold': 0.0,
                     'above_threshold': 0.0,
                     'negative_value': 0.0}

            else:
                current_HNN_dictionary = \
                    {'below_threshold': round(float(
                        number_of_HNN_latencies_below_threshold /
                        total_number_of_HNN_latencies * 100), 2),
                     'above_threshold': round(float(
                         number_of_HNN_latencies_above_threshold /
                         total_number_of_HNN_latencies * 100), 2),
                     'negative_value': round(float(
                         number_of_HNN_latencies_that_are_negative /
                         total_number_of_HNN_latencies * 100), 2)}
            list_of_HNN_timely_availability_dictionaries.append(
                current_HNN_dictionary)

            HNE_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNE"]
            current_HNE_dictionary = {}

            total_number_of_HNE_latencies = HNE_latencies["data_latency"].size

            number_of_HNE_latencies_below_threshold = HNE_latencies.loc[(
                HNE_latencies["data_latency"] <= threshold) &
                (HNE_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNE_latencies_above_threshold = HNE_latencies.loc[(
                HNE_latencies["data_latency"] > threshold) &
                (HNE_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNE_latencies_that_are_negative = HNE_latencies.loc[
                HNE_latencies["data_latency"] == -1]["data_latency"].size
            if total_number_of_HNN_latencies == 0:
                current_HNE_dictionary = \
                    {'below_threshold': 0.0,
                     'above_threshold': 0.0,
                     'negative_value': 0.0}

            else:
                current_HNE_dictionary = \
                    {'below_threshold': round(float(
                        number_of_HNE_latencies_below_threshold /
                        total_number_of_HNE_latencies * 100), 2),
                     'above_threshold': round(float(
                         number_of_HNE_latencies_above_threshold /
                         total_number_of_HNE_latencies * 100), 2),
                     'negative_value': round(float(
                         number_of_HNE_latencies_that_are_negative /
                         total_number_of_HNE_latencies * 100), 2)}
            list_of_HNE_timely_availability_dictionaries.append(
                current_HNE_dictionary)

            HNZ_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNZ"]
            current_HNZ_dictionary = {}

            total_number_of_HNZ_latencies = HNZ_latencies["data_latency"].size

            number_of_HNZ_latencies_below_threshold = HNZ_latencies.loc[(
                HNZ_latencies["data_latency"] <= threshold) &
                (HNZ_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNZ_latencies_above_threshold = HNZ_latencies.loc[(
                HNZ_latencies["data_latency"] > threshold) &
                (HNZ_latencies["data_latency"] != -1)]["data_latency"].size
            number_of_HNZ_latencies_that_are_negative = HNZ_latencies.loc[
                HNZ_latencies["data_latency"] == -1]["data_latency"].size
            if total_number_of_HNN_latencies == 0:
                current_HNZ_dictionary = \
                    {'below_threshold': 0.0,
                     'above_threshold': 0.0,
                     'negative_value': 0.0}

            else:
                current_HNZ_dictionary = \
                    {'below_threshold': round(float(
                        number_of_HNZ_latencies_below_threshold /
                        total_number_of_HNZ_latencies * 100), 2),
                     'above_threshold': round(float(
                         number_of_HNZ_latencies_above_threshold /
                         total_number_of_HNZ_latencies * 100), 2),
                     'negative_value': round(float(
                         number_of_HNZ_latencies_that_are_negative /
                         total_number_of_HNZ_latencies * 100), 2)}
            list_of_HNZ_timely_availability_dictionaries.append(
                current_HNZ_dictionary)

            current_dataframe_date = arrow.get(
                latency_dataframe.iloc[0].startTime).format('YYYY-MM-DD')
            current_dataframe_date_dateobject = arrow.get(
                current_dataframe_date, 'YYYY-MM-DD').date()
            timely_availability_percentage_array_days_axis.append(
                current_dataframe_date_dateobject)
    HNN_timely_availability_percentage_dataframe = pd.DataFrame(
        list_of_HNN_timely_availability_dictionaries)
    HNE_timely_availability_percentage_dataframe = pd.DataFrame(
        list_of_HNE_timely_availability_dictionaries)
    HNZ_timely_availability_percentage_dataframe = pd.DataFrame(
        list_of_HNZ_timely_availability_dictionaries)
    return HNN_timely_availability_percentage_dataframe,\
        HNE_timely_availability_percentage_dataframe,\
        HNZ_timely_availability_percentage_dataframe,\
        timely_availability_percentage_array_days_axis
