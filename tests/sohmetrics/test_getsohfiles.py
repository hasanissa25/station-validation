from stationverification.utilities import sohmetrics
import logging

# flake8: noqa


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
    logging.info(f'test_results: {testresults}')
    assert testresults == ['tests/data/apollo/archive/miniseed/2022/01/10/QW.QCC01..LCQ.2022.010',
                           'tests/data/apollo/archive/miniseed/2022/01/11/QW.QCC01..LCQ.2022.011']
