# flake8:noqa
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities.timely_availability_plot import get_timely_availability_arrays
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes

import logging


def test_get_timely_availability_arrays(latency_parameters_nanometrics, latency_test_files_nanometrics, latency_test_files_nanometrics_negative_latency):
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    HNN_timely_availability_percentage_array,\
        HNE_timely_availability_percentage_array, \
        HNZ_timely_availability_percentage_array,\
        timely_availability_percentage_array_days_axis = \
        get_timely_availability_arrays(latencies=array_of_daily_latency_dataframes,
                                       threshold=latency_parameters_nanometrics.timely_threshold)

    assert HNN_timely_availability_percentage_array == [
        33.33, 0.0, 33.33]
    assert HNE_timely_availability_percentage_array == [
        100.0, 0.0, 100.0]
    assert HNZ_timely_availability_percentage_array == [
        100.0, 0.0, 100.0]

    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_files_nanometrics_negative_latency,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    HNN_timely_availability_percentage_array,\
        HNE_timely_availability_percentage_array, \
        HNZ_timely_availability_percentage_array,\
        timely_availability_percentage_array_days_axis = \
        get_timely_availability_arrays(latencies=array_of_daily_latency_dataframes,
                                       threshold=latency_parameters_nanometrics.timely_threshold)

    assert HNN_timely_availability_percentage_array == [
        0.0]
    assert HNE_timely_availability_percentage_array == [
        0.0]
    assert HNZ_timely_availability_percentage_array == [
        80.0]
