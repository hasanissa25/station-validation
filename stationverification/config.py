from functools import lru_cache
from enum import Enum

from pydantic import BaseSettings


class LogLevels(Enum):
    DEBUG: str = 'DEBUG'
    INFO: str = 'INFO'
    WARNING: str = 'WARNING'
    ERROR: str = 'ERROR'


class BaseAppSettings(BaseSettings):

    LATENCY_DIRECTORY: str = "from_the_config_file/latency"
    MINISEED_DIRECTORY: str = "from_the_config_file/miniseed"
    SOH_DIRECTORY: str = "from_the_config_file/soh"

    class Config:
        env_prefix = 'VALIDATION_'


@lru_cache()
def get_default_parameters() -> BaseAppSettings:
    return BaseAppSettings()
