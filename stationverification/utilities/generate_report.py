'''
This module collects data from the ISPAQ-generated CSV files and generates a
report based on the values within

Classes
-------
StationMetricData:
    Object used to store and manage the output of ISPAQ's data quality tests

Functions
---------
gather_stats:
    Generates and populates StationMetricData object to be used for reporting

report:
    Evalutates the values for each metric for each station in the station_dict
    and give them a Pass or Fail. Creates a json file containing the results.
    The results will also be logged at the INFO level to a file specified, or
    to the screen if no file is specified.

'''
from stationverification.utilities import exceptions
from datetime import date, timedelta
import os
from .metric_handler import metric_handler, check_metric_exists
import json
from typing import Optional
import logging
import pandas as pd
from pandas.core.frame import DataFrame
# from stationverification import CONFIG
from .latency import latencyreport
from . import sohmetrics
from configparser import ConfigParser
from typing import Any, Dict


class StationMetricData():
    '''
    This class is used to retrieve metric data from the csv files that are
    generated by ISPAQ and grant access to it on-demand.

    Properties
    ----------
    station: str
        The station code for the station whose metric data is stored within
    results: Dataframe
        A pandas dataframe to store the data from ISPAQ-generated CSV files

    Functions
    ---------
    __init__:
        Initialize the class by passing it a station name
    populate:
        Load a CSV file and concatinate the data into the results Dataframe
    get_networks:
        Returns a list of networks from the ISPAQ results
    get_stations:
        Returns a list of all stations belonging to a specific network
    get_channels:
        Returns a list of the channels belonging to a station
    get_metricNames:
        Returns a list of metrics that have values stored in the Datafame
    get_values:
        Return the values for a given metric for a given channel

    '''

    def __init__(self):
        '''
        Initialize the StationMetricData object
        '''
        self.results: DataFrame = pd.DataFrame()

    def populate(
        self,
        filename: str
    ):
        '''
        Load a csv file and concatinate the data within to the results
        Dataframe

        Parameters
        ----------
        filename: str
            The path to the csv file to process
        '''
        # Read the specified csv file into a dataframe
        filedf = pd.read_csv(
            filename,
            # Use the start date as the index
            index_col='start',
            parse_dates=['start']
        )

        # Split the target field
        filedf[['network', 'station', 'location', 'channel', 'quality']] = \
            filedf['target'].str.split('.', expand=True)

        # Drop the end, target, location and quality fields
        filedf.drop(
            ['end', 'target', 'location', 'quality'], axis=1, inplace=True)

        # Concatinate the results to the dataframe
        self.results = pd.concat([self.results, filedf], sort=False)
        self.results.dropna(subset=['value'], inplace=True)

    def get_networks(self) -> list:
        '''
        Get a list of networks

        Returns
        -------
        list:
            A list of all the networks stored in the dataframe
        '''
        # Raise an exception if no network column is found in the df
        if 'network' not in self.results:
            raise ValueError(
                'Failed to load results from Ispaq. Check csv folder')
        else:
            # Get a list of all values of the networks column, excluding
            # duplicates
            networks = list(set(self.results['network']))
            return networks

    def get_stations(self, network: str) -> list:
        '''
        Get a list of the stations in a network

        Parameters
        ----------
        network: str
            The network to search for

        Returns
        -------
        list:
            A list of the stations in a network
        '''
        # Raise an exception if no station column is found
        if 'station' not in self.results:
            raise ValueError(
                'Failed to load results from Ispaq. Check csv folder')
        else:
            # Get a list of all unique values in the station column, filtered
            # by a specific network code
            df = self.results[self.results.network == network]
            stations = list(set(df['station']))
            return stations

    def get_channels(self, network: str, station: str) -> list:
        '''
        Get a list of the channels at the station

        Parameters
        ----------
        network: str
            The network to search for

        station: str
            The station to search for

        Returns
        -------
        list:
            A list of the channels at the station
        '''
        # Raise an exception if the channel column is not present
        if 'channel' not in self.results:
            raise ValueError(
                'Failed to load results from Ispaq. Check csv folder')
        else:
            # Get a list of all channels for the specified station
            df = self.results[self.results['network'] == network]
            df = df[df['station'] == station]
            channels = list(set(df['channel']))
            return channels

    def get_metricNames(self) -> list:
        '''
        Get a list of the metrics that ISPAQ returned values for

        Returns
        -------
        list:
            A list of the metrics ISPAQ returned values for
        '''
        # Raise an exception if the metricName column is missing
        if 'metricName' not in self.results:
            raise ValueError(
                'Failed to load results from Ispaq. Check csv folder')
        else:
            # Get a list of the values in the metricName column, excluding
            # duplicates
            metricNames = list(set(self.results['metricName']))
            return metricNames

    def get_values(
        self,
        metric: str,
        network: str = None,
        station: str = None,
        channel: str = None

    ) -> list:
        '''
        Given a channel code and a metric name, return the list of values that
        match

        Parameters
        ----------
        channel: str
            The name of the channel to find results for
        metric: str
            The name of the metric to find results for

        Returns
        -------
        list:
            A list of the values that ISPAQ returned for the specific metric
            and channel specified
        '''
        # Filter the df by the metricName specified
        results = self.results[self.results.metricName == metric]

        # If a network is specified, filter by the network code
        if network is not None:
            results = results[results.network == network]

        # If a station is specified, filter by the station code
        if station is not None:
            results = results[results.station == station]

        # If a channel is specified, filter by the channel code
        if channel is not None:
            results = results[results.channel == channel]
        return list(results.value)


def gather_stats(
    start: date,
    snlc: str,
    stop: date = None,
    metrics: Optional[str] = 'eew_test',
    ispaq_output_directory: Optional[str] = './ispaq_outputs',
) -> StationMetricData:
    '''
    This function locates the csv files that were generated by running ISPAQ
    and then calls populate_dict for each one

    Parameters
    ----------
    start: date
        The start date that should be in the filenames of the ISPAQ-generated
        csv files
    stop: date
        If the testing period is more than one day, the date before this value
        will be in the filenames we're looking for.
    station: str
        The station code to look for csv files for
    metrics: str, optional
        The alias for the group of metrics selected from the ISPAQ preference
        files. This is also part of the filename for the csv files generated.
        Unless the -M option is specified when running the program, the
        default is used.
        Default: eew_test
    ispaqoutdir: str, Optional
        The directory to check for a csv folder. Only implemented for testing

    Returns
    -------
    StationMetricData:
        A class that contains a dataframe full of the results from running
        ISPAQ
    '''
    ispaqoutdir = ispaq_output_directory
    # Determine the filenames of the files generated.
    if (stop and start == stop + timedelta(days=-1)) or stop is None:
        # If the time period is only one day, the filenames only contain
        #  a single date
        basic_filename = f'{ispaqoutdir}/csv/{metrics}_{snlc}_{start}_\
simpleMetrics.csv'
        psd_filename = f'{ispaqoutdir}/csv/{metrics}_{snlc}_{start}_\
PSDMetrics.csv'
        sample_filename = f'{ispaqoutdir}/csv/{metrics}_{snlc}_{start}_\
sampleRateMetrics.csv'
    else:
        # If the time period is more than one day, filenames contain start and
        #  end date
        basic_filename = f'{ispaqoutdir}/csv/{metrics}_{snlc}_{start}_\
{(stop + timedelta(days=-1))}_simpleMetrics.csv'
        psd_filename = f'{ispaqoutdir}/csv/{metrics}_{snlc}_{start}_\
{(stop + timedelta(days=-1))}_PSDMetrics.csv'
        sample_filename = f'{ispaqoutdir}csv/{metrics}_{snlc}_{start}_\
{(stop + timedelta(days=-1))}_sampleRateMetrics.csv'

    # Initialize the StationMetricData object that will contain the data
    smd = StationMetricData()

    # If a file exists with the basic_filename, gather the data from it
    if os.path.exists(basic_filename):
        smd.populate(basic_filename)
    else:
        logging.warning(f'{basic_filename} not found. Check that \
basicStats metrics are specified in ispaq preference file under {metrics}')
    if os.path.exists(psd_filename):
        smd.populate(psd_filename)
    else:
        logging.warning(f'{psd_filename} not found. Check that psd_derived \
metrics are specified in ispaq preference file under {metrics}')
    if os.path.exists(sample_filename):
        smd.populate(sample_filename)

    if len(smd.get_metricNames()) < 1:
        raise FileNotFoundError(
            'No results from Ispaq found. Please check ISPAQ_TRANSCRIPT.log')

    return smd


def report(
    combined_latency_dataframe_for_all_days_dataframe: DataFrame,
    typeofinstrument: str,
    network: str,
    station: str,
    stationmetricdata: StationMetricData,
    start: date,
    end: date,
    thresholds: ConfigParser,
    soharchive: str,
) -> dict:
    '''
    Function used to generate a report about station data quality, evaluating
    the values calculated by ISPAQ and giving them a Pass or Fail

    Parameters
    ----------
    network: str
        The network code for the station

    station: str
        The station code of the station to report on

    stationmetricdata: StationMetricData
        A class that contains a dataframe full of the results from running
        ISPAQ

    start: date
        The start date of the test period

    end: date
        The end date of the test period, non-inclusive

    latencyFiles: str
        The path to the latency statistic files

    thresholds: ConfigParser
        ConfigParser object containing threshold preferences

    soharchive: str
        The path to the soh files driectory

    Returns
    -------
    dict:
        A dictionary containing the report information in a json structure.
        This is returned for unittesting.

    '''
    # Initialize a dictionary to populate with result, to be converted to json
    json_dict: Dict[str, Any] = {}
    json_dict['network_code'] = network
    json_dict['station_code'] = station
    json_dict['start_date'] = start.strftime("%Y-%m-%d")
    json_dict['end_date'] = end.strftime("%Y-%m-%d")
    json_dict['channels'] = {}

    # Loop through each channel in the station
    channels = stationmetricdata.get_channels(network=network, station=station)
    metrics = stationmetricdata.get_metricNames()
    for channel in channels:
        code = channel
        # Add the channel name to the json_dict dictionary to be
        # converted to json
        json_dict['channels'][code] = {}
        json_dict['channels'][code]['metrics'] = {}
        for metric in metrics:
            # Get the values for the metric and hand it off to the
            # metric_handler to recieve a pass or fail grade
            if not check_metric_exists(metric):
                continue
            values = stationmetricdata.get_values(
                network=network,
                station=station,
                channel=channel,
                metric=metric)
            result = metric_handler(
                metric, values, start, thresholds)
            logging.info(f"Metric being ran: {metric}")
            logging.info(f"Values being ran: {values}")
            logging.info(f"Outputted results: {result}")
            # If the result value is false, also log the reason
            # Add the metrics and results to a dictionary to be converted to
            # json
            json_dict['channels'][code]['metrics'][metric] = {}
            json_dict['channels'][code]['metrics'][metric]['passed'] = \
                result.result
            json_dict['channels'][code]['metrics'][metric]['details'] = \
                result.details
            json_dict['channels'][code]['metrics'][metric]['values'] = list(
                values)

    try:
        json_dict = latencyreport(
            combined_latency_dataframe_for_all_days_dataframe=combined_latency_dataframe_for_all_days_dataframe,  # noqa
            network=network,
            station=station,
            json_dict=json_dict,
            timely_threshold=thresholds.getfloat(
                'thresholds', 'data_timeliness', fallback=3),
            timely_percent=thresholds.getfloat(
                'thresholds', 'timely_data_percentage', fallback=98.0),
        )
    except FileNotFoundError as e:
        logging.error(e)
        logging.warning('Skipping latency report.')

    json_report_with_soh_results = \
        add_soh_results_to_report(network=network,
                                  station=station,
                                  startdate=start,
                                  enddate=end,
                                  directory=soharchive,
                                  typeofinstrument=typeofinstrument,
                                  json_dict=json_dict,
                                  thresholds=thresholds)
    # Setup JSson report

    if start == end - timedelta(days=1):
        filename = f'{network}.{station}-{start}-validation_results.json'
    else:
        filename = f'{network}.{station}-{start}_{end}-validation_results.json'

    # Write the json dictionary to a json file
    if not os.path.isdir('./stationvalidation_output'):
        os.mkdir('./stationvalidation_output')
    with open(f'./stationvalidation_output/{filename}', 'w+') as file:
        json.dump(json_report_with_soh_results, file, indent=2)

    # Return the report information in json format
    return json_report_with_soh_results


def add_soh_results_to_report(network: str,
                              station: str,
                              startdate: date,
                              enddate: date,
                              directory: str,
                              typeofinstrument: str,
                              json_dict: dict,
                              thresholds: ConfigParser):
    try:
        # Get a list of "LCE" channel sohmetric files and merge the \
        # resulting streams before passing them to check_timing_quality()
        clock_offset_sohfiles = sohmetrics.getsohfiles(network=network,
                                                       station=station,
                                                       startdate=startdate,
                                                       enddate=enddate,
                                                       channel="LCE",
                                                       directory=directory)
        clock_offset_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                clock_offset_sohfiles)
        results = sohmetrics.check_clock_offset(
            list_of_streams=clock_offset_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'clock_offset', fallback=0.100),
            startdate=startdate,
            enddate=enddate,
            network=network,
            station=station
        )

        if results is not None:
            json_dict['clock_offset'] = {}
            json_dict['clock_offset']['passed'] = results.passed
            json_dict['clock_offset']['values'] = results.results
            if results.passed is False:
                json_dict['clock_offset']['details'] = results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LCE data does not exist. Skipping clock offset metric.')

    try:
        # Get a list of "LCQ" channel sohmetric files and merge the resulting \
        # streams before passing them to check_timing_quality()
        timing_quality_sohfiles = sohmetrics.getsohfiles(network=network,
                                                         station=station,
                                                         startdate=startdate,
                                                         enddate=enddate,
                                                         channel="LCQ",
                                                         directory=directory)
        timing_quality_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                timing_quality_sohfiles)
        results = sohmetrics.check_timing_quality(
            list_of_streams=timing_quality_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'timing_quality', fallback=70.0),
            startdate=startdate, enddate=enddate, network=network,
            station=station,

        )

        if results is not None:
            json_dict['timing_quality'] = {}
            json_dict['timing_quality']['passed'] = results.passed
            json_dict['timing_quality']['values'] = results.results
            if results.passed is False:
                json_dict['timing_quality']['details'] = results.details
            # plot the timing quality results

    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LCQ data does not exist. Skipping timing quality metric.')
    try:
        # Get a list of "GST" channel sohmetric files and merge the resulting \
        # streams before passing them to check_clock_locked()
        check_clock_locked_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="GST",
                                   directory=directory)
        check_clock_locked_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                check_clock_locked_sohfiles)
        results = sohmetrics.check_clock_locked(
            list_of_streams=check_clock_locked_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'clock_locked', fallback=6),
            startdate=startdate
        )

        if results is not None:
            json_dict['clock_locked'] = {}
            json_dict['clock_locked']['passed'] = results.passed
            json_dict['clock_locked']['values'] = results.results
            if results.passed is False:
                json_dict['clock_locked']['details'] = results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'GST data does not exist. Skipping clock locked metric.')
    try:
        # Get a list of "GNS" channel sohmetric files and merge the resulting \
        # streams before passing them to check_clock_locked()
        check_number_of_satellites_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="GNS",
                                   directory=directory)
        check_number_of_satellites_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                check_number_of_satellites_sohfiles)
        results = sohmetrics.check_number_of_satellites(
            list_of_streams=check_number_of_satellites_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'satellites_locked', fallback=6),
            startdate=startdate
        )

        if results is not None:
            json_dict['satellites_locked'] = {}
            json_dict['satellites_locked']['passed'] = results.passed
            # Since were getting the average of a list of size 1, \
            # were only returning the first element of the list
            json_dict['satellites_locked']['values'] = results.results
            if results.passed is False:
                json_dict['satellites_locked']['details'] = results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'GNS data does not exist. Skipping number of satellites metric.')
    return json_dict

# Needs to be refactored as this will not work with the current version of
# station verification
# def bulk_report(
#     stationmetricdata: StationMetricData,
#     hdf5_files: str,
#     outputdir: str,
#     start: date,
#     end: date = None,
#     thresholds: Optional[str] = CONFIG,
# ) -> str:
#     '''
#     Loops through all networks and stations in a StationMetricData object and
#     generates a report for each, returns a path to the reports

#     Parameters
#     ----------

#     stationmetricdata: StationMetricData
#         Object containing results from ISPAQ tests

#     hdf5_files: str
#     start: date
#         The date to preform the test for
#     '''
#     year = start.year
#     month = start.month
#     if month < 10:
#         month = f'0{month}'
#     day = start.day
#     if day < 10:
#         day = f'0{day}'

#     if end is None:
#         end = start + timedelta(days=+1)

#     # Determine the correct directory to store the reports
#     path = f'{outputdir}/{year}/{month}/{day}'
#     if not os.path.isdir(path):
#         os.makedirs(path)
#     # Generate report for each station
#     endDate: date = start + timedelta(days=+1)
#     for network in stationmetricdata.get_networks():
#         for station in stationmetricdata.get_stations(network):
#             report(network=network,
#                    station=station,
#                    stationmetricdata=stationmetricdata,
#                    start=start,
#                    endDate=endDate,
#                    latencyFiles=hdf5_files,
#                    thresholds=thresholds,
#                    sohdirectory=path,
#                    outputdir=outputdir)

#     return path
