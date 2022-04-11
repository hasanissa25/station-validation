from stationverification.utilities.metric_handler import metric_handler


def test_check_spikes(testdata: dict):
    '''
    Test the check_spikes function
    '''

    # Check for passing result
    result = metric_handler(
        'spikes', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []
    # Check for failing result
    result = metric_handler(
        'spikes', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Spikes flag set 11 times on 2021-01-01',
                              'Spikes flag set 11 times on 2021-01-03',
                              'Spikes flag set 12 times on 2021-01-05']
