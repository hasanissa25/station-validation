from stationverification.utilities.metric_handler import metric_handler


def test_check_max_overlap(testdata: dict):
    '''
    Test the check_max_overlap function
    '''
    # Check for passing result
    result = metric_handler(
        'max_overlap', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'max_overlap', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.details == ['Max overlap of 11 seconds detected on 2021-01-01',
                              'Max overlap of 11 seconds detected on 2021-01-03',
                              'Max overlap of 12 seconds detected on 2021-01-05']
    assert result.result is False
