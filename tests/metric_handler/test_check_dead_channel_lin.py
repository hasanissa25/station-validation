from stationverification.utilities.metric_handler import metric_handler


def test_check_dead_channel_lin(testdata: dict):
    '''
    Test the check_dead_channel_lin function
    '''

    # Check for passing result

    result = metric_handler(
        'dead_channel_lin', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'dead_channel_lin', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == [
        'Channel too linear on 2021-01-02',
        'Channel too linear on 2021-01-04']
