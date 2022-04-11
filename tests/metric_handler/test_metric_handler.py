import pytest

from stationverification.utilities.metric_handler import metric_handler
from stationverification.utilities import exceptions


def test_metric_handler(testdata: dict):
    '''
    Test the metric_handler function
    '''
    # Check with valid metric name
    result = metric_handler(
        'amplifier_saturation', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with invalid metric name
    with pytest.raises(exceptions.MetricHandlerError):
        metric_handler(
            'nonexisting_metric', testdata["data"][1],
            testdata["start"], testdata["config"])
