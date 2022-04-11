from stationverification.utilities.metric_handler import metric_handler


def test_check_suspect_time_tag(testdata: dict):
    '''
    Test the check_suspect_time_tag function
    '''
    # Check for passing result
    result = metric_handler(
        'suspect_time_tag', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'suspect_time_tag', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Suspect time tag flag set on 2021-01-01',
                              'Suspect time tag flag set on 2021-01-03',
                              'Suspect time tag flag set on 2021-01-05']
