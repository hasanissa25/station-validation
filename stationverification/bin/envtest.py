import logging
from stationverification.config import get_default_parameters
from stationverification.utilities.fetch_arguments_envtest \
    import fetch_arguments_env_test
logging.basicConfig(
    format='%(asctime)s envTest: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    # Setting up a queue for processors to push their results to if needed
    user_inputs = fetch_arguments_env_test()
    parameters = get_default_parameters()
    logging.info(f'user_inputs {user_inputs}')
    if user_inputs.latency_directory is None:
        latency_directory = parameters.LATENCY_DIRECTORY
    if user_inputs.miniseed_directory is None:
        miniseed_directory = parameters.MINISEED_DIRECTORY
    if user_inputs.soh_directory is None:
        soh_directory = parameters.SOH_DIRECTORY
    logging.info(f"latency directory {latency_directory}")
    logging.info(f"miniseed_directory {miniseed_directory}")
    logging.info(f"soh_directory {soh_directory}")
