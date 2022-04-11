from stationverification.utilities.metric_handler import metric_handler


def test_check_num_spikes(testdata: dict):
    '''
    Test the check_num_spikes function
    '''

    # Check for passing result
    result = metric_handler(
        'num_spikes', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'num_spikes', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 spikes detected on 2021-01-01',
                              '11 spikes detected on 2021-01-01',
                              '12 spikes detected on 2021-01-05']
