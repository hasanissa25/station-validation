from stationverification.utilities.metric_handler import metric_handler


def test_check_timing_quality(testdata: dict):
    '''
    Test the check_timing_quality function
    '''
    # Check for passing result
    result = metric_handler(
        'timing_quality', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'timing_quality', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == [
        'Timing quality 30% on 2021-01-01', 'Timing quality 30% on 2021-01-03']
