# flake8:noqa
import pytest
from datetime import date


class GatherStatsParameters(dict):
    @property
    def snlc(self) -> list:
        return self["snlc"]

    @property
    def start(self) -> bool:
        return self["start"]

    @property
    def stop(self) -> str:
        return self["stop"]

    @property
    def metrics(self) -> list:
        return self["metrics"]

    @property
    def ispaq_output_directory(self) -> list:
        return self["ispaq_output_directory"]


@pytest.fixture(scope="session")
def gather_stats_parameters() -> GatherStatsParameters:
    return GatherStatsParameters(snlc="QW.QCC02.x.Hxx",
                                 start=date(2022, 4, 1),
                                 stop=date(2022, 4, 4),
                                 metrics="eew_test",
                                 ispaq_output_directory="tests/generate_report/ispaq_outputs"
                                 )
