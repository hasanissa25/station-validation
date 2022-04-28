'''
Python script used to produce latency plots for the given period.

usage: stationverificationlatency [-h] -T instrumentType -N NETWORK -S STATION\
     -d STARTDATE -e ENDDATE -l LatencyDirectory

optional arguments:
    -h, --help            show this help message and exit
    -N network, --network NETWORK
                        The station's unique network code. Ex. QW
    -S STATION, --station STATION
                        The station's unique code. Ex. QCC001
    -d STARTDATE, --startdate STARTDATE
                        The first date of the verification period. Must be in
                        YYYY-MM-DD format
    -e ENDDATE, --enddate ENDDATE
                        The end of the verification period. Data will be
                        tested for each day from the start date up to but not
                        including the end date. Must be in YYYY-MM-DD format.
    -t THRESHOLDS, --thresholds THRESHOLDS
                        The path to the preference file containing the
                        thresholds to test the metrics against.
    -l LatencyDirectory, --latency LatencyDirectory
                        The directory containing latency files
    -T TYPEOFINSTRUMENT, --typeofinstrument TYPEOFINSTRUMENT
                        type of instrument used, APOLLO or GURALP
    -U UPLOADTOS3, --uploadresultstos3 UPLOADTOS3
                        Whether or not to upload results to the S3 bucket.\
    -b NAMEOFS3BUCKET, --s3bucketname NAMEOFS3BUCKET
                        To which bucket to upload in S3
    -B S3PATHTOSAVETO, --s3bucketpathtosaveto S3PATHTOSAVETO
                        Which 'directory' in S3 to save to
 True or False
Functions:
----------
main()
    The main fuction, which takes care of calling the other functions
'''
import argparse
import json
import os
import subprocess
import logging
from dateutil import parser as dateparser  # type: ignore
from datetime import date, timedelta  # type: ignore
from stationverification import CONFIG
from configparser import ConfigParser
from stationverification.utilities.\
    calculate_total_availability_for_nanometrics\
    import calculate_total_availability_for_nanometrics
from stationverification.utilities.generate_CSV_from_failed_latencies import\
    generate_CSV_from_failed_latencies

from stationverification.utilities.latency import (
    populate_json_with_latency_info)
from stationverification.utilities.get_latencies import get_latencies
from stationverification.utilities.latency_line_plot import latency_line_plot
from stationverification.utilities.latency_log_plot import latency_log_plot
from stationverification.utilities.timely_availability_plot import \
    timely_availability_plot
from stationverification.utilities.upload_results_to_s3 import \
    upload_results_to_s3
from stationverification.utilities.get_latency_files import get_latency_files
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class TimeSeriesError(Exception):
    '''
    Error to be raised if the enddate specified is before or the same as the
    startdate
    '''

    def __init__(self, msg):
        super().__init__(msg)


def main():
    '''
    The Main function.

    Returns
    -------
        JSON file containing the results of the stationvalidation tests,
        Latency line plot for each day of the validation period
        Latency log plot for the validation period
        CSV file of failed latencies
        A Timely Availability Plot of the validation period

    '''
    # Create argparse object to handle user arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-b",
        "--s3bucketname",
        help="To which bucket to upload in S3",
        type=str,
        default="eew-validation-data"
    )
    argsparser.add_argument(
        "-B",
        "--s3bucketpathtosaveto",
        help="Which 'directory' in S3 to save to",
        type=str,
        default="validation_results"
    )
    argsparser.add_argument(
        "-d",
        "--startdate",
        help="The first date of the verification period. Must be in YYYY-MM-DD \
format",
        type=str,
        required=True
    )
    argsparser.add_argument(
        "-e",
        "--enddate",
        help="The end of the verification period. Data will be tested for each \
day from the start date up to but not including the end date. Must be in \
YYYY-MM-DD format.",
        type=str,
        required=True
    )

    argsparser.add_argument(
        '-l',
        '--latency',
        required=True,
        help='The directory containing the latency data.',
        type=str,
    )

    argsparser.add_argument(
        '-L',
        '--logfile',
        default=None,
        help='To log to a file instead of stdout, specify the filename.',
        type=str
    )

    argsparser.add_argument(
        '-N',
        '--network',
        help='The network code. I.e: QW',
        required=True,
        type=str,
    )
    argsparser.add_argument(
        '-o',
        '--outputdir',
        required=True,
        help='Output directory to store results in. If none is specified, the \
current directory is used.',
        default='./station_validation_latency_results'
    )

    argsparser.add_argument(
        '-S',
        '--station',
        help='The station code. I.e: QCC02',
        required=True,
        type=str,
    )

    argsparser.add_argument(
        '-t',
        '--thresholds',
        default=CONFIG,
        help='Overrides the default config file.',
        type=str
    )
    argsparser.add_argument(
        '-T',
        '--typeofinstrument',
        help='type of instrument used, APOLLO or GURALP',
        required=True,
        type=str
    )
    argsparser.add_argument(
        '-U',
        '--uploadresultstos3',
        help='True, or False. If set to True, the results will be \
automatically uploaded to s3 bucket',
        type=bool
    )
    args = argsparser.parse_args()

    station = args.station
    network = args.network
    startdate = (dateparser.parse(args.startdate, yearfirst=True)).date()
    enddate = (dateparser.parse(args.enddate, yearfirst=True)).date()
    latencyFiles = args.latency
    typeofinstrument = args.typeofinstrument
    outputdir = args.outputdir
    thresholds = ConfigParser()
    thresholds.read(args.thresholds)
    uploadresultstos3 = args.uploadresultstos3
    bucketName = args.s3bucketname
    s3directory = args.s3bucketpathtosaveto
    json_dict = {
        "channels": {
            "HNN": {},
            "HNE": {},
            "HNZ": {}
        }}
    if startdate > enddate:
        raise TimeSeriesError('Enddate must be after startdate.')
    elif startdate == enddate:
        raise TimeSeriesError('Enddate is not inclusive. To test for one day, set \
the enddate to the day after the startdate')
    logging.info("Fetching latency files..")
    files = get_latency_files(typeofinstrument=typeofinstrument,
                              network=network,
                              station=station,
                              path=latencyFiles,
                              startdate=startdate,
                              enddate=enddate)
    logging.info("Populating latency data..")
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes = get_latencies(
            typeofinstrument=typeofinstrument,
            files=files,
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate)
    logging.info("Calculating total availability..")
    total_availability = calculate_total_availability_for_nanometrics(files)
    logging.info("Generating CSV of failed latencies..")
    generate_CSV_from_failed_latencies(
        latencies=combined_latency_dataframe_for_all_days_dataframe,
        station=station,
        network=network,
        startdate=startdate,
        enddate=enddate,
        timely_threshold=thresholds.getfloat(
            'thresholds', 'data_timeliness', fallback=3),)
    logging.info("Generating timely availability plot..")
    timely_availability_plot(latencies=array_of_daily_latency_dataframes,
                             station=station,
                             startdate=startdate,
                             enddate=enddate,
                             network=network,
                             timely_threshold=thresholds.getfloat(
                                 'thresholds', 'data_timeliness', fallback=3))
    logging.info("Generating latency log plots..")

    latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,  # noqa
                     station=station,
                     startdate=startdate,
                     enddate=enddate,
                     typeofinstrument=typeofinstrument,
                     network=network,
                     timely_threshold=thresholds.getfloat(
                         'thresholds', 'data_timeliness', fallback=3),
                     total_availability=total_availability)
    logging.info("Generating latency line plots..")
    latency_line_plot(latencies=array_of_daily_latency_dataframes,
                      station=station,
                      startdate=startdate,
                      network=network,
                      timely_threshold=thresholds.getfloat(
                          'thresholds', 'data_timeliness', fallback=3))
    logging.info("Generating JSON report..")

    populate_json_with_latency_info(
        json_dict=json_dict,
        combined_latency_dataframe_for_all_days_dataframe=combined_latency_dataframe_for_all_days_dataframe,  # noqa
        network=network, station=station,
        timely_threshold=thresholds.getfloat(
                'thresholds', 'data_timeliness', fallback=3),
        timely_percent=thresholds.getfloat(
                'thresholds', 'timely_data_percentage', fallback=98.0)
    )

    dump_json_report(startdate=startdate,
                     enddate=enddate,
                     network=network,
                     station=station,
                     json_dict=json_dict)
    logging.info("Cleaning up directory..")

    cleanup_directory(startdate=startdate,
                      enddate=enddate,
                      network=network,
                      station=station,
                      outputdir=outputdir)
    if uploadresultstos3 is True:
        logging.info("Uploading to S3 bucket..")
        if startdate == enddate - timedelta(days=1):
            validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}'
        else:
            validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}-{enddate}'
        upload_results_to_s3(path_of_folder_to_upload=validation_output_directory,  # noqa
                             bucketName=bucketName,
                             s3directory=s3directory)


def dump_json_report(startdate: date,
                     enddate: date,
                     network: str,
                     station: str,
                     json_dict: dict):
    if startdate == enddate - timedelta(days=1):
        json_file_name = f'{network}.{station}.{startdate}_report'
    else:
        json_file_name = f'{network}.{station}.{startdate}_\
{(enddate + timedelta(days=-1))}_report'
    if not os.path.isdir('./stationvalidation_output'):
        os.mkdir('./stationvalidation_output')

    with open(f'./stationvalidation_output/{json_file_name}.json', 'w+')\
            as file:
        json.dump(json_dict, file, indent=2)


def cleanup_directory(startdate: date,
                      enddate: date,
                      outputdir: str,
                      network: str,
                      station: str,
                      ):
    if startdate == enddate - timedelta(days=1):
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}'
    else:
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}-{enddate}'
    # Create the directory if it doesn't already exist
    if not os.path.isdir(validation_output_directory):
        subprocess.getoutput(
            f'sudo makedir {validation_output_directory}')
    subprocess.getoutput(
        f'sudo mv ./stationvalidation_output/* {validation_output_directory}')  # noqa
    subprocess.getoutput(
        "rmdir './stationvalidation_output'")
