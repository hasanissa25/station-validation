# Hasan: Remove
import argparse
from typing import Optional


class UserInput(dict):

    @property
    def latency_directory(self) -> list:
        return self["latency_directory"]


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
    args = argsparser.parse_args()

    latency_directory = args.latency_directory
    return UserInput(latency_directory=latency_directory)
