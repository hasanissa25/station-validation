# flake8:noqa
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities.timely_availability_plot import get_timely_availability_arrays
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes

import logging
import pandas as pd


def test_get_timely_availability_arrays(latency_parameters_nanometrics, latency_parameters_nanometrics_timely_availability, latency_test_file_nanometrics_timely_availability_test):
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_file_nanometrics_timely_availability_test,
            network=latency_parameters_nanometrics_timely_availability.network,
            station=latency_parameters_nanometrics_timely_availability.station)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    HNN_timely_availability_percentage_dataframe,\
        HNE_timely_availability_percentage_dataframe,\
        HNZ_timely_availability_percentage_dataframe,\
        timely_availability_percentage_array_days_axis = \
        get_timely_availability_arrays(latencies=array_of_daily_latency_dataframes,
                                       threshold=latency_parameters_nanometrics.timely_threshold)
    assert float(
        HNN_timely_availability_percentage_dataframe.iloc[0]["below_threshold"]) == 50.0
