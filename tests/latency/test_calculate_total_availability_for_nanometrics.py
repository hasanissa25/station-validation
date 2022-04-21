# flake8:noqa
import logging

from stationverification.utilities.calculate_total_availability_for_nanometrics import calculate_total_availability_for_nanometrics


def test_calculate_total_availability_for_nanometrics(latency_test_files: list):
    total_availability = calculate_total_availability_for_nanometrics(
        latency_test_files)
    assert total_availability == 26.96
