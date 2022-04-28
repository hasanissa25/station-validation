# flake8=noqa
import subprocess

from build import logging
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo


def test_get_latencies_from_apollo(latency_parameters_nanometrics, latency_test_file_nanometrics_over_3_packets):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes = get_latencies_from_apollo(
            files=latency_test_file_nanometrics_over_3_packets,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
    assert combined_latency_dataframe_for_all_days_dataframe.loc[
        "QW.QCC02.HNE.2022-04-03T00:00:00.000000000Z.max"].data_latency == 3.5
    assert combined_latency_dataframe_for_all_days_dataframe.loc[
        "QW.QCC02.HNZ.2022-04-03T00:00:00.000000000Z.min"].data_latency == 2.6
