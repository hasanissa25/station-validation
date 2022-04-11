from stationverification.utilities.metric_handler import metric_handler


def test_check_pct_below_nlnm(testdata: dict):
    '''
    Test the check_pct_below_nlnm function
    '''

    # Check for passing result
    result = metric_handler(
        'pct_below_nlnm', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'pct_below_nlnm', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% noise below the New Low Noise Model']
