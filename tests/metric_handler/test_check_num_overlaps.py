from stationverification.utilities.metric_handler import metric_handler


def test_check_num_overlaps(testdata: dict):
    '''
    Test the check_num_overlaps function
    '''

    # Check for passing result
    result = metric_handler(
        'num_overlaps', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'num_overlaps', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 overlaps detected on 2021-01-01',
                              '11 overlaps detected on 2021-01-03',
                              '12 overlaps detected on 2021-01-05']
