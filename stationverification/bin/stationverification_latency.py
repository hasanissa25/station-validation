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
import logging
import os
import subprocess
from configparser import ConfigParser
from datetime import date, timedelta  # type: ignore

from dateutil import parser as dateparser  # type: ignore

from stationverification import CONFIG
from stationverification.utilities.latency import latencyreport
from stationverification.utilities.upload_results_to_s3 import \
    upload_results_to_s3

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

    latencyreport(typeofinstrument=typeofinstrument,
                  network=network,
                  station=station,
                  startdate=startdate,
                  enddate=enddate,
                  path=latencyFiles,
                  json_dict=json_dict,
                  timely_threshold=thresholds.getfloat(
                      'thresholds', 'data_timeliness', fallback=3),
                  timely_percent=thresholds.getfloat(
                      'thresholds', 'timely_data_percentage', fallback=98.0))
    logging.info("Cleaning up directory..")

    cleanup_directory_after_latency_call(startdate=startdate,
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


def cleanup_directory_after_latency_call(startdate: date,
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
            f"mkdir -p {validation_output_directory}")
    subprocess.getoutput(
        f"mv ./stationvalidation_output/* {validation_output_directory}")  # noqa
    subprocess.getoutput(
        "rm -rf ./stationvalidation_output")
