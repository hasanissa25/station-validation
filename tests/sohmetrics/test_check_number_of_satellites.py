from datetime import date
import logging
from typing import List
from stationverification.utilities import sohmetrics
import obspy


def test_check_number_of_satellites(list_of_streams: List[obspy.Stream],
                                    passing_threshold: float = 20.0,
                                    failing_threshold: float = 30.0,
                                    startdate: date = date(2021, 1, 1)):
    '''
    Checks the average number of satellites locked for each day for a station

    Returns:
    bool
        Indicates if the metric passed

    string
        Text indicating the reason why the metric may have failed

    list
        List of the results for the metric
    '''
    logging.info('Check number of satellites for the first list of streams')
    # Average number of satellites locked was below threshold
    results = \
        sohmetrics.check_number_of_satellites(
            list_of_streams, threshold=passing_threshold,
            startdate=startdate)
    logging.info(f'results of number of satellites {results.results}')
    assert results.passed
    assert results.results == [20.0, 70.0]

    # Average number of satellites locked was above threshold
    logging.info('Check number of satellites for the second list of streams')

    results = \
        sohmetrics.check_number_of_satellites(
            list_of_streams, threshold=failing_threshold,
            startdate=startdate)
    logging.info(f'results of number of satellites {results.results}')

    assert not results.passed
    assert results.results == [20.0, 70.0]
