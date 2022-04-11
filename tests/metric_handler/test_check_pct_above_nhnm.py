from stationverification.utilities.metric_handler import metric_handler


def test_check_pct_above_nhnm(testdata: dict):
    '''
    Test the check_pct_above_nhnm function
    '''

    # Check for passing result
    result = metric_handler(
        'pct_above_nhnm', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'pct_above_nhnm', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% noise above the New High Noise Model']
