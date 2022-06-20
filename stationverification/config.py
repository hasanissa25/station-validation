# flake8:noqa
from functools import lru_cache
from typing import Any
from pydantic import BaseSettings
from stationverification import CONFIG, ISPAQ_PREF


class BaseAppSettings(BaseSettings):
    # Default Archives
    ISPAQ_LOCATION: str = "/home/ec2-user/ispaq/run_ispaq.py"

    APOLLO_LATENCY_ARCHIVE: str = "/apollo/archive/latency/"
    APOLLO_MINISEED_ARCHIVE: str = "/apollo/archive/miniseed/"
    APOLLO_SOH_ARCHIVE: str = "/apollo/archive/soh/"

    GURALP_LATENCY_ARCHIVE: str = "/guralp/archive/latency/"
    GURALP_MINISEED_ARCHIVE: str = "/guralp/archive/miniseed/"
    GURALP_SOH_ARCHIVE: str = "/guralp/archive/soh/"

    # Default Parameters
    STATION_CONFIG: Any = None
    METRICS: str = "eew_test"
    PDF_INTERVAL: str = "aggregated"
    S3_BUCKET_NAME: str = "eew-validation-data"
    S3_DIRECTORY: str = "validation_results"
    OUTPUT_DIRECTORY: str = "/validation"

    # Default Config Files

    STATION_URL: str = "http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=channel&nodata=404"

    PREFERENCE_FILE: str = ISPAQ_PREF
    THRESHOLDS: str = CONFIG

    # GitLab
    GITLAB_URL: str = "http://gitlab.seismo.nrcan.gc.ca"
    PROJECT_TOKEN: Any = "gJ-TxBSSMYBrsxhh9jze"
    PROJECT_ID: int = 10

    class Config:
        env_prefix = 'VALIDATION_'


@lru_cache()
def get_default_parameters() -> BaseAppSettings:
    return BaseAppSettings()
