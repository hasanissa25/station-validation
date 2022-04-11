from stationverification.utilities.generate_report import gather_stats
from datetime import date


def test_gather_stats(testdata):
    '''
    Function to test the gather_stats function and StationMetricData class
    '''
    smd = gather_stats(
        date(2021, 7, 20),
        date(2021, 7, 23),
        'QCQ',
        ispaqoutdir=testdata)
    assert 'CN' in smd.get_networks()
    assert 'QCQ' in smd.get_stations('CN')
    assert 'pct_above_nhnm' in smd.get_metricNames()
    assert 'num_gaps' in smd.get_metricNames()
