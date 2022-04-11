from datetime import date
from typing import List
from stationverification.utilities import sohmetrics
import obspy

# flake8: noqa


def test_check_clock_locked(list_of_streams: List[obspy.Stream],
                            list_of_streams_clock_locked: List[obspy.Stream],
                            list_of_streams_clock_locked_mix:
                            List[obspy.Stream],
                            threshold: float = 2.0,
                            startdate: date = date(2021, 1, 1)):
    '''
    Check the number of times the clock is locked for a specific station every
        day.

    Returns:
    bool
        Indicates if the metric passed

    string
        Text indicating the reason why the metric may have failed

    list
        List of the results for the metric
    '''
    # # Clock was unlocked more than threshold limit
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams_clock_locked,
        startdate=startdate,
        threshold=threshold)
    assert not results.passed
    assert results.results == [3.0, 4.0]
    assert results.details == ['Clock unlocked 3 times on 2021-01-01. [threshold: 2.0]',
                               'Clock unlocked 4 times on 2021-01-02. [threshold: 2.0]']

    # Results had a mix of below and above threshold
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams_clock_locked_mix,
        startdate=startdate,
        threshold=threshold)
    assert results.details == ['Clock unlocked 3 times on 2021-01-01. [threshold: 2.0]',
                               'Clock unlocked 4 times on 2021-01-02. [threshold: 2.0]']
    assert not results.passed

    # Clock was unlocked less than threshold limit
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams,
        startdate=startdate,
        threshold=threshold)
    assert results.passed
    assert results.results == [0.0, 0.0]
