'''
A module that contains utilities to extract latency values from HDF5 format
files and report on them
'''
import logging
import subprocess
import json
import os
import numpy as np
from typing import List, Tuple
from datetime import date, timedelta

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import matplotlib.dates as mdates

import pandas as pd
from pandas.core.frame import DataFrame
from pandas.plotting import register_matplotlib_converters
from stationverification.utilities.get_latencies_from_apollo \
    import get_latencies_from_apollo


from stationverification.utilities.julian_day_converter import \
    datetime_to_year_and_julian_day
from tests.latency.test_scripts.isolated_components.\
    test_calculate_total_availability import calculate_total_availability

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)


class StationNotInFileException(Exception):
    '''
    Exception to be raised if station in missing from file
    '''

    def __init__(self, msg):
        super().__init__(msg)


def latencyreport(
        typeofinstrument: str,
        network: str,
        station: str,
        startdate: date,
        enddate: date,
        path: str,
        json_dict: dict,
        timely_threshold: float,
        timely_percent: float,
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

    files = getfiles(typeofinstrument=typeofinstrument, network=network,
                     station=station, path=path, startdate=startdate,
                     enddate=enddate)
    logging.info("Populating latency data..")

    # Gather the latency information for the station
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes = getlatencies(
            typeofinstrument=typeofinstrument,
            files=files,
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate)
    # Produce latency plots
    logging.info("Calculating total availability..")

    total_availability = calculate_total_availability(files)
    logging.info("Generating timely availability plot..")

    timely_availability_plot(latencies=array_of_daily_latency_dataframes,
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

    latency_line_plot(latencies=array_of_daily_latency_dataframes,
                      station=station,
                      startdate=startdate,
                      enddate=enddate,
                      typeofinstrument=typeofinstrument,
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


def getfiles(
    typeofinstrument: str,
    network: str,
    path: str,
    station: str,
    startdate: date = (date.today()+timedelta(days=-14)),
    enddate: date = (date.today()+timedelta(days=-1)),

) -> List[str]:
    '''
    Find a list of the latency files for the given time period, network, and \
        station, for either Guralp or Apollo data

    Parameters
    ----------
    typeofinstrument: str
        The type of instrument the data was fetched from 'APOLLO' or 'GURALP'

    network: str
        The network that will be found in the latency file name

    station: str
        The station that will be found in the latency file name

    path: str
        The path to the latency data storage.

    startdate: date
        The date for the beginning of the test. Default: 14 days ago

    enddate: date
        The last date of the test. Default: Yesterday

    Returns
    -------
    list:
        A list of the files for the specified date range
    '''
    files: list = []
    iterdate = startdate
    # Iterate through all the dates in the verification period and collect a
    # list of the associated files
    while iterdate < enddate:
        logging.debug(f'Looking for files for date {iterdate}')
        if typeofinstrument == "APOLLO":
            cmd = f'ls {path}/{iterdate.strftime("%Y/%m/%d")}/\
{network}.{station}.\
{datetime_to_year_and_julian_day(iterdate, typeofinstrument)}.json 2>/dev/null'
        elif typeofinstrument == "GURALP":
            cmd = f'ls {path}/{iterdate.strftime("%Y/%m/%d")}/{network}_\
{station}_*_*_\
{datetime_to_year_and_julian_day(iterdate, typeofinstrument)}.csv \
2>/dev/null'
        output = subprocess.getoutput(
            cmd
        ).split('\n')
        if not output == ['']:
            files.extend(output)
        iterdate += timedelta(days=+1)

    # Throw an exception if no files in the time period are found
    if len(files) <= 0:
        raise FileNotFoundError(f'No files found in {path} for dates between \
{startdate} and {enddate}')
    logging.debug(f'List of files found: {files}')
    return files


def getlatencies(
    typeofinstrument: str,
    files: list,
    network: str,
    station: str,
    startdate=date,
    enddate=date
) -> Tuple[DataFrame, list]:
    '''
    A function that returns a dataframe that includes 'network', 'station', \
        'channel', 'data_latency' columns given CSV or  JSON files

    Parameters
    ----------
    typeofinstrument: str
        The type of instrument the data was fetched from 'APOLLO' or 'GURALP'
    network: str
        The network code for the selected station
    station: str
        The station code for the selected station
    files: str
        A list of Latency files to search, JSON for Apollo, CSV for GUralp

    Returns
    -------
    combined_latency_dataframe_for_all_days_dataframe: Dataframe
        A pandas DataFrame containing a list of latency values for the Station
    array_of_daily_latency_dataframes: list
        A list containing pandas latency dataframes for each day
    '''
    if typeofinstrument == "APOLLO":
        combined_latency_dataframe_for_all_days_dataframe,\
            array_of_daily_latency_dataframes = get_latencies_from_apollo(
                files=files,
                network=network,
                station=station)

    elif typeofinstrument == "GURALP":
        combined_latency_dataframe_for_all_days_dataframe, \
            array_of_daily_latency_dataframes = get_guralp_latencies(
                files=files,
                startdate=startdate,
                enddate=enddate)
    return combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_dataframes,


def percentbelowthreshold(
    station: str,
    latencies: np.array,
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


def get_gaps(
    files: list,
    network: str,
    station: str
) -> pd.DataFrame:
    # Loop through all the files in the list
    df = pd.DataFrame()
    for file in files:
        logging.debug(f'Parsing file {file}')
        # Read the HDF5 file
        hdf = pd.HDFStore(
            file,
            mode='r'
        )

        if '/errors' in hdf.keys():
            hdfdf = hdf.select(key='errors')

            hdfdf = hdfdf[hdfdf.network == network]
            hdfdf = hdfdf[hdfdf.station == station]
            hdfdf = hdfdf[hdfdf.error == 'gap']
            df = df.append(hdfdf, sort=False)

        hdf.close()

    return df


def latency_line_plot(
    latencies: list,
    station: str,
    startdate: date,
    enddate: date,
    typeofinstrument: str,
    network: str,
    timely_threshold: float
):
    '''
    Generates a line plot of latency values for each channel of a station

    Parameters
    ----------
    latencies: list of Pandas dataframes
         Each dataframe contains 'network', 'station', 'channel', 'startTime',
         'data_latency'
    station: str
        The station code. For the title and name of file
    network: str
        The network code. For the title and name of file
    channel: str
        The channel code. For the title and name of file
    startdate: date
        The start date of the validation period
    enddate: date
        The end date of the validation period
    typeofinstrument: str
        Used to annotate the plot
    timely_threshold: float
        Maximum latency for a packet to be considered timely
    return
    -------
    No returned values, but will plot the latency line charts for the given
    validation period

    '''

    # Future versions of pandas will require you to explicitly register
    # matplotlib converters
    register_matplotlib_converters()

    for index, latency_dataframe in enumerate(latencies):
        filename = f'{network}.{station}-{startdate + timedelta(days=index)}\
-latency_line_plot.png'
        HNN_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNN"]
        HNE_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNE"]
        HNZ_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNZ"]
        # Setting up the figure
        fig, axes = plt.subplots(
            3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
        # add a big axis, hide frame
        fig.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', which='both', top=False,
                        bottom=False, left=False, right=False)
        plt.title(
            f'Latencies for {network}.{station} \n \
{startdate + timedelta(days=index)}')
        plt.ylabel("Latency (seconds)")
        threshold = timely_threshold

        axes[0].set_ylim([0, 10])

        # Setting up our data
        x_axis = HNN_latencies.startTime
        x_axis_as_dates = [pd.to_datetime(
            x, infer_datetime_format=True).to_pydatetime() for x in x_axis]
        y_axis = HNN_latencies.data_latency

        # Format the dates on the x-axis
        formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
        axes[0].xaxis.set_major_formatter(formatter)
        locator = mdates.HourLocator()
        axes[0].xaxis.set_major_locator(locator)
        axes[0].tick_params(axis='x', labelrotation=90)

        # Plotting the data
        axes[0].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNN Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=10000, c="green")
        # Show the grid
        axes[0].set_axisbelow(True)
        axes[0].grid(visible=True, which='both', axis='both', linewidth=0.5)
        # Adding the threshold line
        axes[0].axhline(threshold, color='r', linewidth="1",
                        linestyle='--',
                        label=f"Data Timeliness threshold: \
{timely_threshold} seconds")

        legend = axes[0].legend(bbox_to_anchor=(1, 1),
                                loc='upper right', fontsize="9")

        # Setting up the second plot for channel HNE

        axes[1].set_ylim([0, 10])

        # Setting up our data
        x_axis = HNE_latencies.startTime
        x_axis_as_dates = [pd.to_datetime(
            x, infer_datetime_format=True).to_pydatetime() for x in x_axis]
        y_axis = HNE_latencies.data_latency

        # Format the dates on the x-axis
        formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
        axes[1].xaxis.set_major_formatter(formatter)
        locator = mdates.HourLocator()
        axes[1].xaxis.set_major_locator(locator)
        axes[1].tick_params(axis='x', labelrotation=90)

        # Plotting the data
        axes[1].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNE Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=10000, c="green")
        # Show the grid
        axes[1].set_axisbelow(True)
        axes[1].grid(visible=True, which='both', axis='both', linewidth=0.5)
        # Adding the threshold line
        axes[1].axhline(threshold, color='r', linewidth="1",
                        linestyle='--',
                        label=f"Data Timeliness threshold: \
{timely_threshold} seconds")

        legend = axes[1].legend(bbox_to_anchor=(1, 1),
                                loc='upper right', fontsize="9")

        # Setting up the third plot for channel HNZ
        axes[2].set_ylim([0, 10])

        # Setting up our data
        x_axis = HNZ_latencies.startTime
        x_axis_as_dates = [pd.to_datetime(
            x, infer_datetime_format=True).to_pydatetime() for x in x_axis]
        y_axis = HNZ_latencies.data_latency

        # Format the dates on the x-axis
        formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
        axes[2].xaxis.set_major_formatter(formatter)
        locator = mdates.HourLocator()
        axes[2].xaxis.set_major_locator(locator)
        axes[2].tick_params(axis='x', labelrotation=90)

        # Plotting the data
        axes[2].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNZ Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=10000, c="green")
        # Show the grid
        axes[2].set_axisbelow(True)
        axes[2].grid(visible=True, which='both', axis='both', linewidth=0.5)
        # Adding the threshold line
        axes[2].axhline(threshold, color='r', linewidth="1",
                        linestyle='--',
                        label=f"Data Timeliness threshold: \
{timely_threshold} seconds")

        legend = axes[2].legend(bbox_to_anchor=(1, 1),
                                loc='upper right', fontsize="9")
        fig.tight_layout()  # Important for the plot labels to not overlap
        if not os.path.isdir('./stationvalidation_output/'):
            os.mkdir('./stationvalidation_output/')
        plt.savefig(
            f'./stationvalidation_output/{filename}',
            bbox_extra_artists=(legend,),
            bbox_inches='tight')
        plt.close()


def latency_log_plot(
    latencies: DataFrame,
    station: str,
    startdate: date,
    enddate: date,
    typeofinstrument: str,
    network: str,
    timely_threshold: float,
    total_availability: float
):
    '''
    Generates a log plot of latency values for a station

    Parameters
    ----------
    latencies: Pandas dataframe
         Contains 'network', 'station', 'channel', 'startTime', 'data_latency'
    station: str
        The station code. For the title and name of file
    network: str
        The network code. For the title and name of file
    channel: str
        The channel code. For the title and name of file
    startdate: date
        The start date of the validation period
    enddate: date
        The end date of the validation period
    typeofinstrument: str
        Used to annotate the plot
    timely_threshold: float
        Maximum latency for a packet to be considered timely

    return
    -------
    No returned values, but will plot the latency log graph for the given
    validation period

    '''

    # Setting up the file name and plot name based on whether its a one day \
    # validation period or not to know if we include end date or not
    filename = ""
    if startdate == enddate - timedelta(days=1):
        filename = f'{network}.{station}-{startdate}-latency_log_plot.png'
        plottitle = f'Latencies for {network}.{station} \n {startdate}'
    else:
        filename = f'{network}.{station}-{startdate}_to_\
{enddate - timedelta(days=1)}-latency_log_plot.png'
        plottitle = f'Latencies for {network}.{station} \n {startdate} to\
 {enddate - timedelta(days=1)}'

    # Setting up the figure
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)

    ax1 = fig.add_subplot(111)
    ax1.set_title(plottitle)  # Add a title to the axes.
    ax1.set_xlabel('Latency (seconds)')
    ax1.set_ylabel('Occurrences')  # Add a y-label to the axes.
    ax1.set_yscale('log')
    if typeofinstrument == "APOLLO":
        note_content = f'Type of Instrument: TitanSMA\n\
Data availability: {total_availability}%\n\
Average latency:{round(latencies.data_latency.mean(),2)} seconds\n\
Standard deviation: {round(np.std(latencies.data_latency),1)}'
    elif typeofinstrument == "GURALP":
        note_content = f'Instrument: Fortimus\nActual number of data points: \
{latencies.data_latency.size}'

    ax1.text(0, 0.95, note_content, style='italic', fontsize=9,
             transform=ax1.transAxes,
             bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 6})
    ax1.set_axisbelow(True)
    plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

    ax1.hist(
        latencies.data_latency,
        bins=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
              5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10],
        ec='black',
    )

    # Adding the threshold line
    threshold = timely_threshold
    plt.axvline(threshold, color='r', linestyle='--', linewidth=1,
                label=f"Data Timeliness threshold: \
{timely_threshold} seconds")
    legend = ax1.legend(bbox_to_anchor=(1.1, 1),
                        loc='upper right', fontsize="9")
    plt.show()

    fig.tight_layout()  # Important for the plot labels to not overlap
    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    plt.savefig(
        f'./stationvalidation_output/{filename}',
        bbox_extra_artists=(legend,),
        bbox_inches='tight')
    plt.close()


def timely_availability_plot(
    latencies: DataFrame,
    station: str,
    startdate: date,
    enddate: date,
    network: str,
    timely_threshold: float,
):
    register_matplotlib_converters()
    HNN_timely_availability_percentage_array, \
        HNE_timely_availability_percentage_array,\
        HNZ_timely_availability_percentage_array = \
        get_timely_availability_arrays(
            latencies=latencies, threshold=timely_threshold)
    filename = ""
    if startdate == enddate - timedelta(days=1):
        filename = f'{network}.{station}.{startdate}\
.timely_availability_plot.png'
    else:
        filename = f'{network}.{station}-{startdate}_to_\
{enddate - timedelta(days=1)}-timely_availability_plot.png'
    # Setting up the figure
    fig, axes = plt.subplots(
        3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', which='both', top=False,
                    bottom=False, left=False, right=False)
    plt.title(
        f'Timely Availability [%]\n{network}.{station} {startdate}-{enddate}')
    axes[1].set_ylabel("Timely availability [%]")

    # Setting up our X-axis data
    difference = enddate - startdate
    x_axis = np.arange(0, difference.days, 1)
    if len(HNN_timely_availability_percentage_array) == x_axis.size and\
        len(HNE_timely_availability_percentage_array) == x_axis.size and\
            len(HNE_timely_availability_percentage_array) == x_axis.size:
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = startdate + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        axes[0].xaxis.set_major_formatter(formatter)
        axes[0].tick_params(axis='x', labelrotation=90)
        # Format the Y-axis values to be percentages
        axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        loc = plticker.MultipleLocator(base=2)
        axes[0].yaxis.set_major_locator(loc)
        # Plotting the data
        y_axis = HNN_timely_availability_percentage_array
        axes[0].bar(x_axis, [100], color="red")
        axes[0].bar(x_axis, y_axis,
                    label='HNN Timely Availability [%]')
        legend = axes[0].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="9")
        # Show the grid
        axes[0].set_axisbelow(True)
        axes[0].grid(visible=True, which='both', axis='both', linewidth=0.5)
        axes[0].set_ylim(ymin=90, ymax=100)

        # Second plot
        # Setting up our data
        y_axis = HNE_timely_availability_percentage_array
        # Plotting the data
        axes[1].bar(x_axis, [100], color="red")
        axes[1].bar(x_axis, y_axis, label='HNE Timely Availability [%]')
        legend = axes[1].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="9")
        axes[1].yaxis.set_major_locator(loc)
        # Show the grid
        axes[1].set_axisbelow(True)
        axes[1].grid(visible=True, which='both', axis='both', linewidth=0.5)
        axes[1].set_ylim(ymin=90, ymax=100)

        # Third plot
        # Setting up our data
        y_axis = HNZ_timely_availability_percentage_array
        # Plotting the data
        axes[2].bar(x_axis, [100], color="red")
        axes[2].bar(x_axis, y_axis, label='HNZ Timely Availability [%]')
        legend = axes[2].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="9")
        # Show the grid
        axes[2].set_axisbelow(True)
        axes[2].grid(visible=True, which='both', axis='both', linewidth=0.5)
        axes[2].set_ylim(ymin=90, ymax=100)
        axes[2].yaxis.set_major_locator(loc)

        fig.tight_layout()  # Important for the plot labels to not overlap
        if not os.path.isdir('./stationvalidation_output/'):
            os.mkdir('./stationvalidation_output/')
        plt.savefig(
            f'./stationvalidation_output/{filename}',
            bbox_extra_artists=(legend,),
            bbox_inches='tight')
        plt.close()


def get_timely_availability_arrays(
    latencies: DataFrame, threshold: float
) -> Tuple[list, list, list]:
    HNN_timely_availability_percentage_array = []
    HNE_timely_availability_percentage_array = []
    HNZ_timely_availability_percentage_array = []

    for latency_dataframe in latencies:
        HNN_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNN"]
        total_number_of_HNN_latencies = HNN_latencies["data_latency"].size
        number_of_HNN_latencies_below_threshold =\
            HNN_latencies.loc[HNN_latencies["data_latency"]
                              < threshold]["data_latency"].size
        HNN_timely_availability_percentage_array.append(round(float(
            number_of_HNN_latencies_below_threshold /
            total_number_of_HNN_latencies * 100), 2))

        HNE_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNE"]

        total_number_of_HNE_latencies = HNE_latencies["data_latency"].size
        number_of_HNE_latencies_below_threshold =\
            HNE_latencies.loc[HNE_latencies["data_latency"]
                              < threshold]["data_latency"].size
        HNE_timely_availability_percentage_array.append(round(float(
            number_of_HNE_latencies_below_threshold /
            total_number_of_HNE_latencies * 100), 2))
        HNZ_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNZ"]
        total_number_of_HNZ_latencies = HNZ_latencies["data_latency"].size
        number_of_HNZ_latencies_below_threshold =\
            HNZ_latencies.loc[HNZ_latencies["data_latency"]
                              < threshold]["data_latency"].size
        HNZ_timely_availability_percentage_array.append(round(float(
            number_of_HNZ_latencies_below_threshold /
            total_number_of_HNZ_latencies * 100), 2))
    return HNN_timely_availability_percentage_array,\
        HNE_timely_availability_percentage_array, \
        HNZ_timely_availability_percentage_array


def generate_CSV_from_failed_latencies(latencies: DataFrame,
                                       station: str,
                                       network: str,
                                       startdate: date,
                                       enddate: date,
                                       timely_threshold: float
                                       ):
    filename = f'{network}.{station}-{startdate}_to_{enddate}-\
failed_latencies.csv'
    latencies_above_three = latencies.loc[latencies.data_latency
                                          > timely_threshold]
    if 'date' in latencies.columns:
        latencies.drop(
            'date', axis=1, inplace=True)
    latencies_above_three_rounded = latencies_above_three.loc[:,
                                                              ['network',
                                                               'station',
                                                               'channel',
                                                               'startTime',
                                                               'data_latency']]

    latencies_above_three_rounded["data_latency"] = round(
        latencies_above_three_rounded.data_latency.astype(float), 2)

    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    latencies_above_three_rounded.to_csv(
        f'./stationvalidation_output/{filename}', index=False)


def get_apollo_latencies(files: list,
                         network: str,
                         station: str) -> Tuple[DataFrame, list]:
    # Dataframe used to hold latency information for the station
    columns = ('network', 'station', 'channel',
               'startTime', 'data_latency')
    combined_latency_data_for_all_days = {}
    array_of_daily_latency_dataframes = []
    for file in files:
        # Opening JSON file
        json_latency_file = open(file)
        # returns JSON object as a dictionary
        latency_data = json.load(json_latency_file)
        # Storing the data of the current days JSON latency file
        current_day_latency_data = {}
        # Iterating through the json availability array which a string "id",
        # and an array of latency data "Intervals"
        for current_NSC in latency_data['availability']:
            current_id = current_NSC["id"]
            network_station = [network, station]

            # making sure we are looping over the required network station
            # combo, as the current iteration of the latency JSON files,
            # contain all the network and stations in one JSON file
            # for that specific day
            if all(x in current_id for x in network_station):
                # splitting the id column and fetching the network, station
                # and channel values, id originally looks like the following :
                # "QW.QCC01.HNN"
                current_network, current_station, current_channel = \
                    current_NSC['id'].split(
                        '.')
                # looping over the intervals array, which contains all the
                # latency objects in 1 second intervals for a specific NSC
                for current_latency in current_NSC['intervals']:
                    if current_latency["latency"]["maximum"] != -1:
                        # The latency data of all days that we are
                        # iterating over
                        combined_latency_data_for_all_days[current_network +
                                                           "."+current_station
                                                           +
                                                           "."+current_channel
                                                           +
                                                           "." +
                                                           current_latency[
                                                               'startTime']] =\
                            {'network': current_network,
                             'station': current_station,
                             'channel': current_channel,
                             'startTime': current_latency["startTime"],
                             'data_latency':
                             current_latency['latency']['maximum']
                             }
                        # The latency data of only the current day we are
                        # iterating over
                        current_day_latency_data[current_network +
                                                 "."+current_station +
                                                 "."+current_channel +
                                                 "." +
                                                 current_latency['startTime']]\
                            = {'network': current_network,
                               'station': current_station,
                               'channel': current_channel,
                               'startTime': current_latency["startTime"],
                               'data_latency':
                               current_latency['latency']['maximum']
                               }
        json_latency_file.close()
        daily_latency_dataframe = pd.DataFrame(
            data=current_day_latency_data, index=columns).T
        array_of_daily_latency_dataframes.append(
            daily_latency_dataframe)
    combined_latency_dataframe_for_all_days_dataframe = pd.DataFrame(
        data=combined_latency_data_for_all_days, index=columns).T
    return combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes


def get_guralp_latencies(files: list,
                         startdate: date,
                         enddate: date) -> \
        Tuple[DataFrame, list]:
    combined_latency_dataframe_for_all_days_dataframe = pd.DataFrame(
        {'network': [], 'station': [], 'channel': [], "startTime": [],
         'data_latency': []})
    array_of_daily_latency_dataframes = []
    for file in files:
        current_file_dataframe = pd.read_csv(file)

        current_file_dataframe[['network', 'station', "location", 'channel']
                               ] = \
            current_file_dataframe['channel'].str.split('.',
                                                        expand=True)

        current_file_dataframe.rename(
            columns={"channel": "channel",
                     "network latency": "network_latency",
                     "data latency": "data_latency",
                     "network": "network",
                     "station": "station",
                     "location": "location",
                     "timestamp": "startTime"}, inplace=True)
        # Data_latency column is in the format of  "=269/100+6.6", which we \
        # need to split and get the value for
        current_file_dataframe[['data_latency']] = \
            current_file_dataframe['data_latency'].str.extract(
            '=(.*)/').astype(float)/100
        current_file_dataframe['data_latency'] = \
            current_file_dataframe['network_latency'] + \
            current_file_dataframe['data_latency']
        combined_latency_dataframe_for_all_days_dataframe = \
            combined_latency_dataframe_for_all_days_dataframe.append(
                current_file_dataframe[[
                    'network', 'station', 'channel', 'startTime',
                    'data_latency']], sort=False)
    # Populating the daily latency array by looping over the dates in the
    # validation period, and filtering the
    # combined_latency_dataframe_for_all_days_dataframe to only those dates,
    # then creating a dataframe with that dates data
    # We then add that dates dataframe into the daily latency array

    # Adding a column that represents the start time in a YY-MM-DD format, in
    # order to compare it to the current date we are looping over
    combined_latency_dataframe_for_all_days_dataframe_with_datetime = \
        combined_latency_dataframe_for_all_days_dataframe
    combined_latency_dataframe_for_all_days_dataframe_with_datetime["date"] =\
        pd.to_datetime(
        combined_latency_dataframe_for_all_days_dataframe["startTime"],
        infer_datetime_format=True).apply(lambda x: x.strftime('%Y-%m-%d'))

    while startdate < enddate:
        array_of_daily_latency_dataframes.append(
            combined_latency_dataframe_for_all_days_dataframe_with_datetime[
                combined_latency_dataframe_for_all_days_dataframe_with_datetime["date"]  # noqa
                == str(startdate)])
        startdate += timedelta(days=+1)

    if 'date' in\
            combined_latency_dataframe_for_all_days_dataframe_with_datetime.columns:  # noqa
        combined_latency_dataframe_for_all_days_dataframe_with_datetime.drop(
            'date', axis=1, inplace=True)
    return combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes
