from stationverification.utilities.metric_handler import metric_handler

# flake8: noqa


def test_check_num_gaps(testdata: dict):
    '''
    Test the check_num_gaps function
    '''
    # Check with passing data
    result = metric_handler(
        'num_gaps', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with failing data
    result = metric_handler(
        'num_gaps', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 gaps detected on 2021-01-01',
                              '11 gaps detected on 2021-01-03', '12 gaps detected on 2021-01-05']
