from pathlib import Path

ISPAQ_PREF = str(Path(__file__).parent.joinpath(
    'data', 'eew_preferences.txt'))
CONFIG = str(Path(__file__).parent.joinpath(
    'data', 'config.ini'))
XML_CONVERTER = str(Path(__file__).parent.joinpath(
    'data', 'stationxml-seed-converter-2.1.0.jar'))
STATION_XML = str(Path(__file__).parent.joinpath(
    'data', 'stationxml.xml'))

from . import _version
__version__ = _version.get_versions()['version']
