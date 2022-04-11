import logging
from typing import List
from stationverification.utilities import sohmetrics
# flake8: noqa


def test_get_list_of_streams_from_list_of_files(example_files: List[str]):
    list_of_streams = sohmetrics.get_list_of_streams_from_list_of_files(
        example_files)
    logging.info(
        f'list of streams retrieved {list_of_streams}')
    # Get the stream, get the data of the first and only trace, and compare it to the expected data
    assert (list_of_streams[0][0].data == [1, 2, 3]).all()
    assert (list_of_streams[1][0].data == [5, 6, 7]).all()
    assert (list_of_streams[2][0].data == [1, 2, 3, 5, 6, 7]).all()
