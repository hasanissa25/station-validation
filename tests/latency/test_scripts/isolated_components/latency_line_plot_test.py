'''
A module that contains utilities to extract latency values from HDF5 format
files and report on them
'''
import logging
import os
import warnings

from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
from pandas.plotting import register_matplotlib_converters


warnings.filterwarnings("ignore")
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def latency_line_plot_test(
    latencies: list,
    network: str,
    station: str,
    startdate: date,
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
        logging.info("Converting X axis to dates for plot 0")
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
        logging.info("Ploting axes 0")
        axes[0].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNN Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=100000, c="green")
        # Show the grid
        logging.info("Axes 0 is plotted")
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
        logging.info("Converting X axis to dates for plot 1")
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
        logging.info("Ploting axes 1")
        axes[1].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNE Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=100000, c="green")
        logging.info("Axes 1 is plotted")
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
        logging.info("Converting X axis to dates for plot 2")
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
        logging.info("Ploting axes 2")
        axes[2].plot(
            x_axis_as_dates, y_axis,
            marker='o', label='HNZ Latency values', linewidth=1,
            markeredgewidth=1,
            markersize=1, markevery=100000, c="green")
        # Show the grid
        logging.info("Axes 2 is plotted")
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
