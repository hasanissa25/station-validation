from stationverification.utilities.metric_handler import metric_handler


def test_check_digitizer_clipping(testdata: dict):
    '''
    Test the check_digitizer_clipping function
    '''

    # Check for passing result
    result = metric_handler(
        'digitizer_clipping', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'digitizer_clipping', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Overvoltage detected on 2021-01-01',
                              'Overvoltage detected on 2021-01-03', 'Overvoltage detected on 2021-01-05']
