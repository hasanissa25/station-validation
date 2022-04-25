# flake8=noqa
import subprocess

from build import logging
from stationverification.utilities.get_latencies import get_latencies


def test_get_latencies(latency_parameters_nanometrics, latency_test_files_nanometrics):
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes = get_latencies(
            typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station,
            startdate=latency_parameters_nanometrics.startdate,
            enddate=latency_parameters_nanometrics.enddate)
    logging.info(
        f'array_of_daily_latency_dataframes f{array_of_daily_latency_dataframes}')
