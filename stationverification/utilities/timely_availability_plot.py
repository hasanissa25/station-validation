import logging
import os
import warnings

import numpy as np
from typing import Tuple
from datetime import date, timedelta

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker

from pandas.core.frame import DataFrame
from pandas.plotting import register_matplotlib_converters


warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)


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
