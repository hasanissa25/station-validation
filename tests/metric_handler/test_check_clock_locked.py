from stationverification.utilities.metric_handler import metric_handler

# flake8: noqa


def test_check_clock_locked(testdata: dict):
    '''
    Test the check_clock_locked function
    '''

    # Check for passing result
    result = metric_handler(
        'clock_locked', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'clock_locked', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Clock not locked with enough satelites on 2021-01-01',
                              'Clock not locked with enough satelites on 2021-01-02',
                              'Clock not locked with enough satelites on 2021-01-03',
                              'Clock not locked with enough satelites on 2021-01-04']
