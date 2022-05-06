# Hasan: Remove
import argparse
from typing import Optional


class UserInput(dict):

    @property
    def latency_directory(self) -> list:
        return self["latency_directory"]

    @property
    def miniseed_directory(self) -> list:
        return self["miniseed_directory"]

    @property
    def soh_directory(self) -> list:
        return self["soh_directory"]


def fetch_arguments_env_test(ISPAQ_and_latency: Optional[bool] = False) \
        -> UserInput:
    # Create argparse object to handle user arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        '-l',
        '--latency_directory',
        help='The directory containing the latency data.',
        type=str,
    )
    argsparser.add_argument(
        '-m',
        '--miniseed_directory',
        help='The directory containing the latency data.',
        type=str,
    )
    argsparser.add_argument(
        '-s',
        '--soh_directory',
        help='The directory containing the latency data.',
        type=str,
    )
    args = argsparser.parse_args()

    latency_directory = args.latency_directory
    miniseed_directory = args.miniseed_directory
    soh_directory = args.soh_directory

    return UserInput(latency_directory=latency_directory,
                     miniseed_directory=miniseed_directory,
                     soh_directory=soh_directory)
