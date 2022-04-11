from stationverification.utilities.metric_handler import metric_handler

# flake8: noqa


def test_check_calibration_signal(testdata: dict):
    '''
    Test the check_calibration_signal
    '''
    # Check for passing result
    result = metric_handler(
        'calibration_signal', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'calibration_signal', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Calibration signal flag set on 2021-01-01',
                              'Calibration signal flag set on 2021-01-03', 'Calibration signal flag set on 2021-01-05']
