'''
A module that contains utilities to extract latency values from HDF5 format
files and report on them
'''
import logging
import warnings

import numpy as np
from typing import Any
from datetime import date

from pandas.core.frame import DataFrame

from stationverification.utilities.\
    calculate_total_availability_for_nanometrics\
    import calculate_total_availability_for_nanometrics
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes
from stationverification.utilities.generate_CSV_from_failed_latencies import\
    generate_CSV_from_failed_latencies
from stationverification.utilities.get_latencies import get_latencies
from stationverification.utilities.get_latency_files import get_latency_files
from stationverification.utilities.latency_line_plot import latency_line_plot
from stationverification.utilities.latency_log_plot import latency_log_plot

from stationverification.utilities.timely_availability_plot import \
    timely_availability_plot

warnings.filterwarnings("ignore")
logging.basicConfig(
    filename="std.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def latencyreport(
        typeofinstrument: str,
        network: str,
        station: str,
        startdate: date,
        enddate: date,
        path: str,
        json_dict: dict,
        timely_threshold: float,
        timely_percent: float
) -> dict:
    '''
    Function to report on latency information about a station

    Parameters
    ----------
    typeofinstrument: str
        The instrument type that we are fetching data from: "APOLLO" / "GURALP"
    network: str
        The network code for the station
    station: str
        The station code to be reported on

    startdate: date
        The first date to check latency for

    enddate: date
        The last date to check latency for

    path: str
        The path to the directory that stores latency information for either \
            Guralp or Apollo instruments

    timely_threshold: float
        The latency goal in seconds that latency is expected to be below

    timely_percent: float
        The percentage of latency values that should be below the
        timely_threshold

    json_dict: str
        The dictionary object to store the results of the report in

    Returns
    -------
        dict: The dictionary object containing the results of the report
    '''
    # Collect the list of files to collect latency information from
    logging.info("Fetching latency files..")

    files = get_latency_files(typeofinstrument=typeofinstrument,
                              network=network,
                              station=station,
                              path=path, startdate=startdate,
                              enddate=enddate)
    logging.info("Populating latency data..")

    # Gather the latency information for the station
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects_max_latency_only, \
        array_of_daily_latency_objects_all_latencies = get_latencies(
            typeofinstrument=typeofinstrument,
            files=files,
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate)
    # Produce latency plots
    logging.info("Calculating total availability..")
    total_availability = calculate_total_availability_for_nanometrics(files)
    logging.info(
        "Calling convert_array_of_latency_objects_into_array_of_dataframes for\
 array_of_daily_latency_objects_max_latency_only")
    array_of_daily_latency_dataframes_max_latency_only = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_max_latency_only)
    logging.info(
        "Finished Calling convert_array_of_latency_objects_into_array_of_dataframes\
for array_of_daily_latency_objects_max_latency_only")
    logging.info(
        "Calling convert_array_of_latency_objects_into_array_of_dataframes for\
 array_of_daily_latency_objects_all_latencies")
    array_of_daily_latency_dataframes_all_latencies = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)
    logging.info(
        "Finished Calling convert_array_of_latency_objects_into_array_of_dataframes\
for array_of_daily_latency_objects_all_latencies")

    logging.info("Generating timely availability plot..")
    timely_availability_plot(
        latencies=array_of_daily_latency_dataframes_all_latencies,
        station=station,
        startdate=startdate,
        enddate=enddate,
        network=network,
        timely_threshold=timely_threshold,
    )
    logging.info("Generating latency log plots..")

    latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,  # noqa
                     station=station,
                     startdate=startdate,
                     enddate=enddate,
                     typeofinstrument=typeofinstrument,
                     network=network,
                     timely_threshold=timely_threshold,
                     total_availability=total_availability
                     )
    logging.info("Generating latency line plots..")

    latency_line_plot(
        latencies=array_of_daily_latency_dataframes_max_latency_only,
        station=station,
        startdate=startdate,
        network=network,
        timely_threshold=timely_threshold
    )
    logging.info("Generating CSV of failed latencies..")

    generate_CSV_from_failed_latencies(
        latencies=combined_latency_dataframe_for_all_days_dataframe,
        station=station,
        network=network,
        startdate=startdate,
        enddate=enddate,
        timely_threshold=timely_threshold
    )
    logging.info("Generating JSON report..")

    final_json_dict = populate_json_with_latency_info(
        json_dict=json_dict,
        combined_latency_dataframe_for_all_days_dataframe=combined_latency_dataframe_for_all_days_dataframe,  # noqa 501
        network=network,
        station=station,
        timely_threshold=timely_threshold,
        timely_percent=timely_percent,
    )
    return final_json_dict


def populate_json_with_latency_info(
        json_dict: dict,
        combined_latency_dataframe_for_all_days_dataframe: DataFrame,
        network: str,
        station: str,
        timely_threshold: float,
        timely_percent: float,
):

    channels = json_dict['channels'].keys()
    logging.debug(f'List of channels in the json_dict: {channels}')
    # Calculate average latency for the individual channels and\
    #  timely_percentage and failed latencies
    for channel in channels:
        average = combined_latency_dataframe_for_all_days_dataframe[
            combined_latency_dataframe_for_all_days_dataframe.channel
            == channel].data_latency.mean()
        logging.info(
            f'Average latency for channel {channel} is \
{round(float(average), 3)} seconds')  # :.3f
        json_dict['channels'][channel]['latency'] = {}
        json_dict['channels'][channel]['latency']['average_latency'] = \
            round(float(average), 3)
        below_threshold = percentbelowthreshold(
            f'{station}.{channel}',
            combined_latency_dataframe_for_all_days_dataframe
            [combined_latency_dataframe_for_all_days_dataframe.channel ==
             channel].data_latency,
            timely_threshold)
        json_dict['channels'][channel]['latency']['timely_availability'] = \
            round(float(below_threshold), 2)
        latencies_for_current_channel = \
            combined_latency_dataframe_for_all_days_dataframe[
                combined_latency_dataframe_for_all_days_dataframe.channel
                == channel]
        number_of_latencies_for_current_channel = \
            latencies_for_current_channel.data_latency.size
        number_of_failed_latencies_for_current_channel = \
            latencies_for_current_channel[
                latencies_for_current_channel["data_latency"] > 3]\
            .data_latency.size
        json_dict['channels'][channel]['latency']['total_latencies'] = \
            number_of_latencies_for_current_channel
        json_dict['channels'][channel]['latency']['failed_latencies'] = \
            number_of_failed_latencies_for_current_channel

    # JSON report calculations
    average = \
        combined_latency_dataframe_for_all_days_dataframe.data_latency.mean()
    logging.info(
        f'Overall average latency for {network}-{station} is \
{round(float(average), 3)} seconds')
    json_dict['station_latency'] = {}
    json_dict['station_latency']['average_latency'] = round(float(average), 3)
    below_threshold = percentbelowthreshold(
        station,
        combined_latency_dataframe_for_all_days_dataframe.data_latency,
        timely_threshold)
    json_dict['station_latency']['timely_availability'] = round(
        float(below_threshold), 2)
    if below_threshold >= timely_percent:
        json_dict['station_latency']['timely_passed'] = True
    else:
        json_dict['station_latency']['timely_passed'] = False
    return json_dict


def percentbelowthreshold(
    station: str,
    latencies: Any,
    threshold: float
) -> float:
    '''
    Function that calculates the percentage of values in an array of latency
    values that are below a specified threshold

    Parameters
    ----------
    station: string
        The code of the station that is being tested, for logging purposes
    latencies: Numpy Array
        The latency values to test against the threshold
    threshold: float
        The maximum latency to test against

    Returns
    -------
    float:
        The percentage of latency values that were below the threshold
    '''
    n = np.count_nonzero(latencies < threshold)
    percent = n / len(latencies) * 100
    logging.info(f'Percent of latencies for {station} below {threshold} \
seconds: {round(float(percent),2)}%')
    return float(percent)
