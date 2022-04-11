from stationverification.utilities.metric_handler import metric_handler


def test_check_max_gap(testdata: dict):
    '''
    Test the check_max_gap function
    '''
    # Check for passing result
    result = metric_handler(
        'max_gap', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'max_gap', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Max gap of 11 seconds detected on 2021-01-01',
                              'Max gap of 11 seconds detected on 2021-01-03',
                              'Max gap of 12 seconds detected on 2021-01-05']
