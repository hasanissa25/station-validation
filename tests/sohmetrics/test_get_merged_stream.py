import numpy as np
import numpy.ma as ma
import pytest
import logging
import obspy

from stationverification.utilities import exceptions, sohmetrics


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
    logging.info(f'mergedstream {mergedstream}')
    merged_stream_data = sohmetrics.get_stream_data_of_merged_streams(
        mergedstream)
    logging.info(f'merged_stream_data {merged_stream_data}')

    expected_trace = np.array([1, 2, 3])

    assert (merged_stream_data == expected_trace).all()

    # Empty stream
    with pytest.raises(exceptions.StreamError):
        sohmetrics.get_merged_stream(
            empty_stream)
