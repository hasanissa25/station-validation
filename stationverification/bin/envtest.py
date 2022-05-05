import logging
from stationverification.utilities.fetch_arguments import fetch_arguments
from stationverification.config import get_default_parameters


def main():
    # Setting up a queue for processors to push their results to if needed
    user_inputs = fetch_arguments()
    parameters = get_default_parameters()
    if user_inputs.latency_directory is None:
        latency_directory = parameters.latency_directory

    logging.info(f"latency directory {latency_directory}")
