# flake8: noqa

import obspy
import pytest
import logging
import numpy as np
import numpy.ma as ma
from typing import List

from stationverification.utilities import exceptions, sohmetrics


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


def test_get_merged_stream(stream_with_gaps: obspy.Stream,
                           stream_without_gaps: obspy.Stream,
                           empty_stream: obspy.Stream):
    # Stream with gaps
    mergedstream = sohmetrics.get_merged_stream(stream_with_gaps)
    merged_stream_data = sohmetrics.get_stream_data_of_merged_streams(
        mergedstream)
    expected_masked_trace = ma.array(
        [1, 2, 3, 4, 5, 6, 7], mask=[0, 0, 0, 1, 0, 0, 0])
    assert (merged_stream_data == expected_masked_trace).all()

    # Stream without gaps
    mergedstream = sohmetrics.get_merged_stream(
        stream_without_gaps)
    merged_stream_data = sohmetrics.get_stream_data_of_merged_streams(
        mergedstream)

    expected_trace = np.array([1, 2, 3])

    assert (merged_stream_data == expected_trace).all()

    # Empty stream
    with pytest.raises(exceptions.StreamError):
        sohmetrics.get_merged_stream(
            empty_stream)


def test_get_stream_data_of_merged_streams(stream_with_gaps: obspy.Stream,
                                           stream_without_gaps: obspy.Stream,
                                           empty_stream: obspy.Stream):
    # Stream with gaps
    logging.info("Stream with gaps before merge", stream_with_gaps)
    stream_with_gaps_merged = sohmetrics.get_merged_stream(stream_with_gaps)
    logging.info("Stream with gaps after merge", stream_with_gaps_merged)

    # Stream without gaps
    logging.info("Stream without gaps before merge", stream_without_gaps)
    stream_without_gaps_merged = sohmetrics.get_merged_stream(
        stream_without_gaps)
    logging.info("Stream without gaps after merge", stream_without_gaps_merged)

    # Empty stream
    # with pytest.raises(exceptions.StreamError):
    #     sohmetrics.get_merged_stream(
    #         empty_stream)
