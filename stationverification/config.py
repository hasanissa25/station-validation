# flake8:noqa
from functools import lru_cache
from typing import Any
from pydantic import BaseSettings
from stationverification import CONFIG, ISPAQ_PREF, STATION_URL


class BaseAppSettings(BaseSettings):
    # Default Archives
    ISPAQ_LOCATION: str = "/home/ec2-user/ispaq/run_ispaq.py"
    LATENCY_ARCHIVE: str = "/apollo/archive/latency/"
    MINISEED_ARCHIVE: str = "/apollo/archive/miniseed/"
    SOH_ARCHIVE: str = "/apollo/archive/soh/"

    # Default Parameters
    STATION_CONFIG: Any = None
    METRICS: str = "eew_test"
    PDF_INTERVAL: str = "aggregated"
    S3_BUCKET_NAME: str = "eew-validation-data"
    S3_DIRECTORY: str = "validation_results"
    OUTPUT_DIRECTORY: str = "/validation"

    # Default Config Files
    PREFERENCE_FILE: str = ISPAQ_PREF
    THRESHOLDS: str = CONFIG
    STATION_URL: str = STATION_URL

    class Config:
        env_prefix = 'VALIDATION_'


@lru_cache()
def get_default_parameters() -> BaseAppSettings:
    return BaseAppSettings()
