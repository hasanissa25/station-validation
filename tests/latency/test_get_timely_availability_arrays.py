# flake8:noqa
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities.timely_availability_plot import get_timely_availability_arrays


def test_get_timely_availability_arrays(latency_parameters_nanometrics, latency_test_files):
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes = get_latencies_from_apollo(
            files=latency_test_files,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    HNN_timely_availability_percentage_array,\
        HNE_timely_availability_percentage_array, \
        HNZ_timely_availability_percentage_array = \
        get_timely_availability_arrays(latencies=array_of_daily_latency_dataframes,
                                       threshold=latency_parameters_nanometrics.timely_threshold)

    assert HNN_timely_availability_percentage_array == [
        33.33, 0.0, 33.33]
    assert HNE_timely_availability_percentage_array == [
        100.0, 0.0, 100.0]
    assert HNZ_timely_availability_percentage_array == [
        100.0, 0.0, 100.0]
