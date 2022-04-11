import obspy
from stationverification.utilities import sohmetrics


def test_getstats(stream_with_gaps: obspy.Stream):
    '''
    Gathers statistics from a SOH miniseed file

    Returns:
        tuple:
            Average, Minimum, and Maximum values for the SOH file
    '''

    stats = sohmetrics.getstats(
        stream=stream_with_gaps)

    assert stats.average == 4
    assert stats.minimum == 1
    assert stats.maximum == 7
