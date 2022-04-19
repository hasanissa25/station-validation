from typing import List
import obspy
from stationverification.utilities import sohmetrics
from datetime import date


def test_check_timing_quality(
        list_of_streams_timing_quality: List[obspy.Stream],
        passing_threshold: float = 5.0,
        failing_threshold: float = 95.0,
        startdate: date = date(2021, 1, 1),
        enddate: date = date(2021, 1, 2),
        network: str = "QW",
        station: str = "QCC02"):
    '''

    Check the timing quality SOH channel and ensure the daily
        averages fall above a specific threshold

    Returns:
        bool
            Indicates if the metric passed

        string
            Text indicating the reason why the metric may have failed

        list
            List of the results for the metric
    '''
    # Timing quality daily average falls above threshold
    results = \
        sohmetrics.check_timing_quality(
            list_of_streams=list_of_streams_timing_quality,
            threshold=passing_threshold,
            startdate=startdate,
            enddate=enddate,
            network=network,
            station=station)

    assert results.passed
    assert results.details == []
    assert results.results == [20.0, 70.0, 17.0]

    # Timing quality daily average falls below threshold
    results = \
        sohmetrics.check_timing_quality(
            list_of_streams=list_of_streams_timing_quality,
            threshold=failing_threshold, startdate=startdate,
            enddate=enddate,
            network=network,
            station=station)

    assert not results.passed
    assert results.details == ['Timing quality below 95.0% on 2021-01-01',
                               'Timing quality below 95.0% on 2021-01-02',
                               'Timing quality below 95.0% on 2021-01-03']
    assert results.results == [20.0, 70.0, 17.0]
