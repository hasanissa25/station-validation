# flake8: noqa

import obspy

from typing import List

from stationverification.utilities import sohmetrics


def test_getsohfiles(sohcriteria: dict):
    '''
    Retrieves a list of the daily SOH channel files for the specified SOH
        channel

    Returns:
        list
            List of files found for the specified station, SOH channel and
              time period
    '''

    testresults = sohmetrics.getsohfiles(
        network=sohcriteria["network"],
        station=sohcriteria["station"],
        channel=sohcriteria["channel"],
        startdate=sohcriteria["startdate"],
        enddate=sohcriteria["enddate"],
        directory=sohcriteria["directory"])
    assert testresults == [
        'tests/data/apollo/archive/soh/2022/04/01/QW.QCC02..LCQ.2022.091']


def test_get_list_of_streams_from_list_of_files(example_files: List[str]):
    list_of_streams = sohmetrics.get_list_of_streams_from_list_of_files(
        example_files)
    assert (list_of_streams[0][0].data == [1, 2, 3]).all()
    assert (list_of_streams[1][0].data == [5, 6, 7]).all()
    assert (list_of_streams[2][0].data == [1, 2, 3, 5, 6, 7]).all()


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
