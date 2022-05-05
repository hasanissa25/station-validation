from functools import lru_cache
from enum import Enum

from pydantic import BaseSettings


class LogLevels(Enum):
    DEBUG: str = 'DEBUG'
    INFO: str = 'INFO'
    WARNING: str = 'WARNING'
    ERROR: str = 'ERROR'


class BaseAppSettings(BaseSettings):

    latency_directory: str = "from_the_config_file/latency"

    class Config:
        env_prefix = 'validation_'


@lru_cache()
def get_default_parameters() -> BaseAppSettings:
    return BaseAppSettings()
