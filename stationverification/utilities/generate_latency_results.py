import logging
from datetime import date
from typing import Any, Optional

from pandas.core.frame import DataFrame
from stationverification.utilities.\
    calculate_total_availability_for_nanometrics import \
    calculate_total_availability_for_nanometrics
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes import \
    convert_array_of_latency_objects_into_array_of_dataframes
from stationverification.utilities.generate_CSV_from_failed_latencies import \
    generate_CSV_from_failed_latencies
from stationverification.utilities.get_latencies import get_latencies
from stationverification.utilities.get_latency_files import get_latency_files
from stationverification.utilities.latency_line_plot import latency_line_plot
from stationverification.utilities.latency_log_plot import latency_log_plot
from stationverification.utilities.timely_availability_plot import \
    timely_availability_plot

logging.basicConfig(
    format='%(asctime)s Latency: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def generate_latency_results(typeofinstrument: str,
                             network: str,
                             station: str,
                             startdate: date,
                             enddate: date,
                             path: str,
                             timely_threshold: float,
                             queue: Optional[Any] = False,) -> DataFrame:
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

    array_of_daily_latency_dataframes_max_latency_only = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_max_latency_only)

    array_of_daily_latency_dataframes_all_latencies = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_all_latencies)

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
    if queue:
        queue.put(combined_latency_dataframe_for_all_days_dataframe)
    return combined_latency_dataframe_for_all_days_dataframe