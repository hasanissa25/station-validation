from datetime import date
import subprocess
from stationverification import XML_CONVERTER
from obspy.io.xseed import Parser
import os
import requests


url = 'http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=channel&nodata=404'  # noqa
request = requests.get(url, allow_redirects=True)

open('stationverification/data/QW.xml', 'wb').write(request.content)

# ISPAQ with merge
ispaqloc = "../ISPAQ/ispaq/run_ispaq.py"

pfile = 'stationverification/data/eew_preferences.txt'

# Apollo
# station = "QW.BCV11.*.H??"
# startdate = date(2022, 6, 1)
# enddate = date(2022, 6, 2)
# miniseedarchive = "tests/data/apolloLocation/archive/miniseed"

# Guralp
station = "QW.QCN08.00.H??"
startdate = date(2022, 6, 1)
enddate = date(2022, 6, 2)
miniseedarchive = "tests/data/guralp/archive/miniseed"

metrics = "eew_test"

station_url = "stationverification/data/QW.xml"

pdfinterval = "aggregated"

# Use IRIS's stationxml-seed-converter java porgram to convert stationxml
# to dataless seed, and then use the obspy parser object to convert to
# RESP file.
# tempfolder = tempfile.TemporaryDirectory(prefix='valdiation')

subprocess.getoutput(f'java -jar {XML_CONVERTER} --input \
{station_url} --output stationverification/data/stationXML.dataless')
pars = Parser("stationverification/data/stationXML.dataless")
if not os.path.isdir("stationverification/data/resp_files"):
    os.mkdir('stationverification/data/resp_files')
pars.write_resp(folder="stationverification/data/resp_files/", zipped=False)

resp_dir = "stationverification/data/resp_files/"


cmd = f'{ispaqloc} -M {metrics} \
    --starttime={startdate} --endtime={enddate} \
     -S {station} -P {pfile} \
        --pdf_interval {pdfinterval} \
        --station_url {station_url} \
        --dataselect_url {miniseedarchive}\
        --resp_dir {resp_dir}'

proc = subprocess.Popen(
    cmd,
    shell=True
)
proc.wait()
