'''
Python script used to check the quality of data coming from new EEW Stations
in order to validate that the stations are suitable for production.

usage: stationverification [-h] -N NETWORK -S STATION -d STARTDATE -e ENDDATE
                           -s STATIONURL -m MINISEEDARCHIVE -l LATENCYARCHIVE
                           -H SOHARCHIVE -i ISPAQLOCATION -T TYPEOFINSTRUMENT

optional arguments:
    -h, --help            show this help message and exit
    -N NETWORK, --network NETWORK
                        The networks unique code. Ex. QW
    -S STATION, --station STATION
                        The station's unique code. Ex. QCQ
    -d STARTDATE, --startdate STARTDATE
                        The first date of the verification period. Must be in
                        YYYY-M-D format
    -e ENDDATE, --enddate ENDDATE
                        The end of the verification period. Data will be
                        tested for each day from the start date up to but not
                        including the end date. Must be in YYYY-MM-DD format.
    -i ISPAQLOCATION, --ispaqlocation ISPAQLOCATION
                        If ispaq is not installed as a package, specify the
                        location of run_ispaq.py
    -l LatencyDirectory, --latency LatencyDirectory
                        The directory containing latency files
    -H SOHDirectory, --soh_archive SOHDirectory
                        The directory containing SOH files
    -m miniseedDirectory, --miniseedarchive miniseedDirectory
                        The directory containing miniseed files
    -s station_url, --station_url station_url
                        FDSN webservice or path to stationXML
    -P PREFERENCEFILE --preference_file PREFERENCEFILE
                        The path to the ISPAQ preference file. Overrides the \
default ispaq config file.
    -p PDFINTERVAL, --pdfinterval PDFINTERVAL
                        time span for PDFs - daily and/or aggregated over the \
                            entire span
    -T TYPEOFINSTRUMENT, --typeofinstrument TYPEOFINSTRUMENT
                        type of instrument used, APOLLO or GURALP
    -U UPLOADTOS3, --uploadresultstos3 UPLOADTOS3
                        Whether or not to upload results to the S3 bucket.\
    -b NAMEOFS3BUCKET, --s3bucketname NAMEOFS3BUCKET
                        To which bucket to upload in S3
    -B S3PATHTOSAVETO, --s3bucketpathtosaveto S3PATHTOSAVETO
                        Which 'directory' in S3 to save to
    -c STATIONCONFIG, --stationconfig STATIONCONFIG
                        Path to the file that contains station information.
 True or False
Functions:
----------
main()
    The main fuction, which takes care of calling the other functions and
    running ISPAQ
'''
import argparse

from dateutil import parser as dateparser
from configparser import ConfigParser

from stationverification import ISPAQ_PREF, CONFIG
from stationverification.utilities.handle_running_ispaq_command import\
    handle_running_ispaq_command

from stationverification.utilities.prepare_ispaq import cleanup
from stationverification.utilities.generate_report import gather_stats, report
from stationverification.utilities.generate_plots import plot_metrics,\
    PlotParameters
from stationverification.utilities.upload_results_to_s3 import \
    upload_results_to_s3


class TimeSeriesError(Exception):
    '''
    Error to be raised if the enddate specified is before or the same as the
    startdate
    '''

    def __init__(self, msg):
        super().__init__(msg)


class MissingConfigOrStationxml(Exception):
    '''
    Exception to be raised if either the stationXML or stationconfig file
    are not included
    '''

    def __init__(self, msg):
        super().__init__(msg)


def main():
    '''
    The Main function.

    Returns
    -------
    {station}_results.json
        A json file containing the results of the stationvalidation tests.

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
        '-c',
        '--stationconfig',
        help='Path to the file that contains station information.',
        type=str,
        default=None
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
        '-f',
        '--fdsnws',
        help='FDSN webservice URL to use. If not specified, then \
--stationconfig must be specified to generate station metadata for Ispaq',
        type=str,
        default=None
    )
    argsparser.add_argument(
        '-H',
        '--soh_archive',
        help='Path to the state of health files',
        required=True,
        type=str,
    )
    argsparser.add_argument(
        '-i',
        '--ispaqlocation',
        required=True,
        help='Specifies the path or alias for the ispaq cmdline tool. Default: \
ispaq',
        type=str
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
        '-m',
        '--miniseedarchive',
        required=True,
        help='The parent directory of the miniseed archive.'
    )
    argsparser.add_argument(
        '-M',
        '--metrics',
        default='eew_test',
        help='Select the group of metrics from the ispaq preference file to run with. \
Default: eew_test',
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
        help='Output directory to store results in. If none is specified, the \
current directory is used.',
        default='./station_validation_results'
    )

    argsparser.add_argument(
        '-p',
        '--pdfinterval',
        help='time span for PDFs: daily and/or aggregated over the entire \
span',
        default="aggregated",
        type=str
    )
    argsparser.add_argument(
        '-P',
        '--preference_file',
        default=ISPAQ_PREF,
        help='The path to the preference file. Overrides the default ispaq\
 file.',
        type=str
    )
    argsparser.add_argument(
        '-s',
        '--station_url',
        help='FDSN webservice or path to stationXML file',
        type=str,
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
    ispaqloc = args.ispaqlocation
    metrics = args.metrics
    pfile = args.preference_file
    thresholds = ConfigParser()
    thresholds.read(args.thresholds)
    fdsnws = args.fdsnws
    latencyFiles = args.latency
    pdfinterval = args.pdfinterval
    station_url = args.station_url
    typeofinstrument = args.typeofinstrument
    miniseedarchive = args.miniseedarchive
    soharchive = args.soh_archive
    outputdir = args.outputdir
    uploadresultstos3 = args.uploadresultstos3
    bucketName = args.s3bucketname
    s3directory = args.s3bucketpathtosaveto
    stationconf = args.stationconfig
    if startdate > enddate:
        raise TimeSeriesError('Enddate must be after startdate.')
    elif startdate == enddate:
        raise TimeSeriesError('Enddate is not inclusive. To test for one day, set \
the enddate to the day after the startdate')
    if stationconf is None and station_url is None:
        raise MissingConfigOrStationxml(
            'Please include either the StationXML file or the Station Config \
file')

    handle_running_ispaq_command(ispaqloc=ispaqloc,
                                 metrics=metrics,
                                 startdate=startdate,
                                 enddate=enddate,
                                 pfile=pfile,
                                 pdfinterval=pdfinterval,
                                 miniseedarchive=miniseedarchive,
                                 network=network,
                                 station=station,
                                 station_url=station_url,
                                 stationconf=stationconf)

    # Read the files generated and populate the dictionary object
    if stationconf is None:
        snlc = f'{network}.{station}.x.Hxx'
    else:
        snlc = f'{station}'
    stationMetricData = gather_stats(
        snlc=snlc,
        start=startdate,
        stop=enddate,
        metrics=metrics)
    # Loop through the channels and create a plot of metrics related to
    # sample data
    # Requires the following metrics in the eew_test line of the
    # eew_preferences.txt file:
    # sample_max, sample_mean, sample_min, sample_median, sample_rms
    for channel in stationMetricData.get_channels(
        network=network,
        station=station
    ):
        plot_metrics(
            PlotParameters(network=network,
                           station=station,
                           channel=channel,
                           stationMetricData=stationMetricData,
                           start=startdate,
                           stop=enddate)

        )

    report(typeofinstrument=typeofinstrument,
           network=network,
           station=station,
           stationmetricdata=stationMetricData,
           start=startdate, end=enddate,
           latencyFiles=latencyFiles,
           thresholds=thresholds,
           soharchive=soharchive,
           )

    # Delete temporary files and links and package the output in a tarball
    if 'temppref' in locals():
        cleanup(
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate,
            outputdir=outputdir)
    else:
        cleanup(
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate,
            outputdir=outputdir)
    if uploadresultstos3 is True:
        upload_results_to_s3(path_of_folder_to_upload=outputdir,
                             bucketName=bucketName,
                             s3directory=s3directory)
