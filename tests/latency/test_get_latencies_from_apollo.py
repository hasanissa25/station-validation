# flake8=noqa
import subprocess

from build import logging
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo


def test_get_latencies_from_apollo(latency_parameters_nanometrics, latency_test_file_over_3_packets):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes = get_latencies_from_apollo(
            files=latency_test_file_over_3_packets,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    logging.info(
        f'array_of_daily_latency_dataframes f{array_of_daily_latency_dataframes}')
