from stationverification.utilities.metric_handler import metric_handler


def test_check_dead_channel_gsn(testdata: dict):
    '''
    Test the check_dead_channel_gsn function
    '''

    # Check for passing result
    result = metric_handler(
        'dead_channel_gsn', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'dead_channel_gsn', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Channel dead on 2021-01-01',
                              'Channel dead on 2021-01-03',
                              'Channel dead on 2021-01-05']
