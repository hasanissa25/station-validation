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
    assert testresults == [
        'tests/data/apollo/archive/soh/2022/04/01/QW.QCC02..LCQ.2022.091']
