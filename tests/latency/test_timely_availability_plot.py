# flake8=noqa
import subprocess
from datetime import date, timedelta
from stationverification.utilities.get_latency_files import get_latency_files

from stationverification.utilities.timely_availability_plot import timely_availability_plot
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes


def test_timely_availability_plot(latency_parameters_nanometrics_timely_availability, latency_test_file_nanometrics_timely_availability_test):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_file_nanometrics_timely_availability_test,
            network=latency_parameters_nanometrics_timely_availability.network,
            station=latency_parameters_nanometrics_timely_availability.station)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    timely_availability_plot(
        latencies=array_of_daily_latency_dataframes,
        network=latency_parameters_nanometrics_timely_availability.network,
        station=latency_parameters_nanometrics_timely_availability.station,
        startdate=latency_parameters_nanometrics_timely_availability.startdate,
        enddate=latency_parameters_nanometrics_timely_availability.enddate,
        timely_threshold=latency_parameters_nanometrics_timely_availability.timely_threshold
    )

    # subprocess.getoutput(
    #     "rm -rf 'stationvalidation_output'")
