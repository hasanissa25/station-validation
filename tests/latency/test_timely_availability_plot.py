# flake8=noqa
import subprocess
from datetime import timedelta

from stationverification.utilities.timely_availability_plot import timely_availability_plot
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes


def test_timely_availability_plot(latency_parameters_nanometrics, latency_test_files_nanometrics):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    timely_availability_plot(
        latencies=array_of_daily_latency_dataframes,
        network=latency_parameters_nanometrics.network,
        station=latency_parameters_nanometrics.station,
        startdate=latency_parameters_nanometrics.startdate,
        enddate=latency_parameters_nanometrics.enddate,
        timely_threshold=latency_parameters_nanometrics.timely_threshold
    )
    # Testing 1 day plot
    timely_availability_plot(
        latencies=array_of_daily_latency_dataframes,
        network=latency_parameters_nanometrics.network,
        station=latency_parameters_nanometrics.station,
        startdate=latency_parameters_nanometrics.startdate,
        enddate=latency_parameters_nanometrics.startdate + timedelta(days=1),
        timely_threshold=latency_parameters_nanometrics.timely_threshold
    )
