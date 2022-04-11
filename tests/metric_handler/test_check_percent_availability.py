from stationverification.utilities.metric_handler import metric_handler


def test_check_percent_availability(testdata: dict):
    '''
    Test the check_percent_availability function
    '''

    # Check for passing result
    result = metric_handler(
        'percent_availability', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'percent_availability', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% data availability']
