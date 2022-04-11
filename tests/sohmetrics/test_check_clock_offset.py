from datetime import date
import logging
from typing import List
from stationverification.utilities import sohmetrics
import obspy


def test_check_clock_offset(list_of_streams: List[obspy.Stream],
                            passing_threshold: float = 90.0,
                            failing_threshold: float = 1,
                            startdate: date = date(2021, 1, 1)):
    '''
    Check the average clock offset for each day.

    Returns:
    bool
        Indicates if the metric passed

    string
        Text indicating the reason why the metric may have failed

    list
        List of the results for the metric
    '''
    # Clock offset passes
    # logging.info('Check clock offset for the first list of streams')
    # results = sohmetrics.check_clock_offset(
    #     list_of_streams, threshold=passing_threshold,
    #     startdate=startdate)
    # assert results.passed
    # assert results.details == "None"
    # assert results.results == [20.0, 70.0]
    # Clock phase error is too high
    # logging.info('Check clock offset for the second list of streams')
    results = sohmetrics.check_clock_offset(
        list_of_streams, threshold=failing_threshold,
        startdate=startdate)
    logging.info(f'results {results}')
    # assert not results.passed
    # assert results.results == [20.0, 70.0]
