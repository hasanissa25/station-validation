# flake8:noqa

from typing import Any, Tuple
import pytest
from datetime import date
import pandas as pd


class LatencyParameters(dict):
    @property
    def type_of_instrument(self) -> list:
        return self["type_of_instrument"]

    @property
    def network(self) -> bool:
        return self["network"]

    @property
    def station(self) -> str:
        return self["station"]

    @property
    def startdate(self) -> list:
        return self["startdate"]

    @property
    def enddate(self) -> list:
        return self["enddate"]

    @property
    def path(self) -> list:
        return self["path"]

    @property
    def json_dict(self) -> list:
        return self["json_dict"]

    @property
    def timely_threshold(self) -> list:
        return self["timely_threshold"]

    @property
    def timely_percent(self) -> list:
        return self["timely_percent"]


@pytest.fixture(scope="session")
def latency_parameters_nanometrics() -> LatencyParameters:
    return LatencyParameters(type_of_instrument="APOLLO",
                             network="QW",
                             station="QCC02",
                             startdate=date(2022, 4, 1),
                             enddate=date(2022, 4, 4),
                             path="tests/data/apollo/archive/latency",
                             json_dict={
                                 "channels": {
                                     "HNN": {},
                                     "HNE": {},
                                     "HNZ": {}
                                 }},
                             timely_threshold=3,
                             timely_percent=98)


@pytest.fixture(scope="session")
def latency_test_files() -> list:
    return ['tests/latency/sample_nanometrics_latency_data_1.json', 'tests/latency/sample_nanometrics_latency_data_2.json', 'tests/latency/sample_nanometrics_latency_data_3.json']


@pytest.fixture(scope="session")
def latency_test_file_over_3_packets() -> list:
    return ['tests/latency/sample_nanometrics_latency_data_4.json']


@pytest.fixture(scope="session")
def latency_dataframe() -> Tuple[Any, date, date]:
    columns = ('network', 'station', 'channel',
               'startTime', 'data_latency')
    latency_data: dict = {}
    latency_data["QW.QCC02.HNZ." + str(date(2022, 4, 1))
                 + ".max"] = {'network': "QW",
                              'station': "QCC02",
                              'channel': "HNZ",
                              'startTime': str(date(2022, 4, 1)),
                              'data_latency': 5}
    latency_data["QW.QCC02.HNZ." + str(date(2022, 4, 2))
                 + ".max"] = {'network': "QW",
                              'station': "QCC02",
                              'channel': "HNZ",
                              'startTime': str(date(2022, 4, 2)),
                              'data_latency': 4}
    latency_data["QW.QCC02.HNZ." + str(date(2022, 4, 3))
                 + ".max"] = {'network': "QW",
                              'station': "QCC02",
                              'channel': "HNZ",
                              'startTime': str(date(2022, 4, 3)),
                              'data_latency': 3}
    latency_data["QW.QCC02.HNZ." + str(date(2022, 4, 4))
                 + ".max"] = {'network': "QW",
                              'station': "QCC02",
                              'channel': "HNZ",
                              'startTime': str(date(2022, 4, 4)),
                              'data_latency': 2.5}
    combined_latency_dataframe_for_all_days = pd.DataFrame(
        data=latency_data, index=columns).T
    return combined_latency_dataframe_for_all_days
