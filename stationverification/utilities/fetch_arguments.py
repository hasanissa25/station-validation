import argparse
from configparser import ConfigParser
from typing import Optional

from dateutil import parser as dateparser  # type: ignore

from stationverification import CONFIG, ISPAQ_PREF
from stationverification.utilities import exceptions


class UserInput(dict):
    @property
    def station(self) -> bool:
        return self["station"]

    @property
    def network(self) -> str:
        return self["network"]

    @property
    def startdate(self) -> list:
        return self["startdate"]

    @property
    def enddate(self) -> list:
        return self["enddate"]

    @property
    def ispaqloc(self) -> list:
        return self["ispaqloc"]

    @property
    def metrics(self) -> list:
        return self["metrics"]

    @property
    def pfile(self) -> list:
        return self["pfile"]

    @property
    def thresholds(self) -> list:
        return self["thresholds"]

    @property
    def latencyFiles(self) -> list:
        return self["latencyFiles"]

    @property
    def pdfinterval(self) -> list:
        return self["pdfinterval"]

    @property
    def station_url(self) -> list:
        return self["station_url"]

    @property
    def typeofinstrument(self) -> list:
        return self["typeofinstrument"]

    @property
    def miniseedarchive(self) -> list:
        return self["miniseedarchive"]

    @property
    def soharchive(self) -> list:
        return self["soharchive"]

    @property
    def outputdir(self) -> list:
        return self["outputdir"]

    @property
    def uploadresultstos3(self) -> list:
        return self["uploadresultstos3"]

    @property
    def bucketName(self) -> list:
        return self["bucketName"]

    @property
    def s3directory(self) -> list:
        return self["s3directory"]

    @property
    def stationconf(self) -> list:
        return self["stationconf"]


def fetch_arguments(ISPAQ_and_latency: Optional[bool] = False) -> UserInput:
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
        required=True if ISPAQ_and_latency else False,
        type=str,
    )
    argsparser.add_argument(
        '-i',
        '--ispaqlocation',
        required=True if ISPAQ_and_latency else False,
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
        required=True if ISPAQ_and_latency else False,
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
        required=True,
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
    # fdsnws = args.fdsnws
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
        raise exceptions.TimeSeriesError('Enddate must be after startdate.')
    elif startdate == enddate:
        raise exceptions.TimeSeriesError('Enddate is not inclusive. To test for one day, set \
the enddate to the day after the startdate')
    if stationconf is None and station_url is None and ISPAQ_and_latency:
        raise exceptions.MissingConfigOrStationxml(
            'Please include either the StationXML file or the Station Config \
file')
    return UserInput(station=station,
                     network=network,
                     startdate=startdate,
                     enddate=enddate,
                     ispaqloc=ispaqloc,
                     metrics=metrics,
                     pfile=pfile,
                     thresholds=thresholds,
                     latencyFiles=latencyFiles,
                     pdfinterval=pdfinterval,
                     station_url=station_url,
                     typeofinstrument=typeofinstrument,
                     miniseedarchive=miniseedarchive,
                     soharchive=soharchive,
                     outputdir=outputdir,
                     uploadresultstos3=uploadresultstos3,
                     bucketName=bucketName,
                     s3directory=s3directory,
                     stationconf=stationconf)
