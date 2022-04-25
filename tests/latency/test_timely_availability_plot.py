# flake8=noqa
import subprocess
from datetime import timedelta

from stationverification.utilities.timely_availability_plot import timely_availability_plot
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo


def test_timely_availability_plot(latency_parameters_nanometrics, latency_test_files_nanometrics):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes = get_latencies_from_apollo(
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
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
