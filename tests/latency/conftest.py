# flake8:noqa

import pytest
from datetime import date


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
def latency_parameters_nanometrics() -> dict:
    return LatencyParameters(type_of_instrument="APOLLO",
                             network="QW",
                             station="QCC02",
                             startdate=date(2022, 4, 1),
                             enddate=date(2022, 4, 2),
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
