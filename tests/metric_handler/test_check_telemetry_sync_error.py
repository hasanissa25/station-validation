from stationverification.utilities.metric_handler import metric_handler


def test_check_telemetry_sync_error(testdata: dict):
    '''
    Test the check_telementry_sync_error function
    '''

    # Check for passing result
    result = metric_handler(
        'telemetry_sync_error', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'telemetry_sync_error', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Telemetry sync error detected on 2021-01-01',
                              'Telemetry sync error detected on 2021-01-03',
                              'Telemetry sync error detected on 2021-01-05']
