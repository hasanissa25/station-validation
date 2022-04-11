from stationverification.utilities.metric_handler import metric_handler

# flake8: noqa


def test_check_amplifier_saturation(testdata: dict):
    '''
    Test the check_amplifier_saturation
    '''
    # Check with passing data
    result = metric_handler(
        'amplifier_saturation', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with failing data
    result = metric_handler(
        'amplifier_saturation', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Amplifier saturation flag set on 2021-01-01', 'Amplifier saturation flag set on 2021-01-03', 'Amplifier saturation flag set on 2021-01-05']
