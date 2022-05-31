import os
import warnings
import logging
from typing import List

from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

from stationverification.utilities.get_timely_availability_arrays\
    import get_timely_availability_arrays

warnings.filterwarnings("ignore")


def timely_availability_plot(
    latencies: List,
    station: str,
    startdate: date,
    enddate: date,
    network: str,
    timely_threshold: float,
):
    register_matplotlib_converters()
    HNN_timely_availability_percentage_dataframe,\
        HNE_timely_availability_percentage_dataframe,\
        HNZ_timely_availability_percentage_dataframe,\
        timely_availability_percentage_array_days_axis = \
        get_timely_availability_arrays(
            latencies=latencies, threshold=timely_threshold)
    logging.info(f'{HNN_timely_availability_percentage_dataframe}')
    logging.info(f'{HNE_timely_availability_percentage_dataframe}')
    logging.info(f'{HNZ_timely_availability_percentage_dataframe}')
    filename = ""
    if startdate == enddate - timedelta(days=1):
        filename = f'{network}.{station}...{startdate}\
.timely_availability_plot.png'
    else:
        filename = f'{network}.{station}...{startdate}_\
{enddate - timedelta(days=1)}.timely_availability_plot.png'
    # Setting up the figure
    fig, axes = plt.subplots(
        3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', which='both', top=False,
                    bottom=False, left=False, right=False)
    plt.title(
        f'Timely Availability [%]\n{network}.{station} {startdate}_{enddate}')
    axes[1].set_ylabel("Timely availability [%]")

    # Setting up our X-axis data
    x_axis = timely_availability_percentage_array_days_axis
    if len(HNN_timely_availability_percentage_dataframe) == len(x_axis) and\
        len(HNE_timely_availability_percentage_dataframe) == len(x_axis) and\
            len(HNZ_timely_availability_percentage_dataframe) == len(x_axis)\
            and len(x_axis) != 0:
        # Format the dates on the x-axis
        formatter = mdates.DateFormatter("%Y-%m-%d")
        axes[0].xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        axes[0].xaxis.set_major_locator(locator)
        axes[0].tick_params(axis='x', labelrotation=90)
        # Format the Y-axis values to be percentages
        axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        loc = plticker.MultipleLocator(base=2)
        axes[0].yaxis.set_major_locator(loc)
        # Plotting the data
        y_axis_below_threshold = \
            HNN_timely_availability_percentage_dataframe.below_threshold
        y_axis_negative_values = \
            HNN_timely_availability_percentage_dataframe.below_threshold\
            + HNN_timely_availability_percentage_dataframe.negative_value

        axes[0].bar(x_axis, [100], color="red")
        axes[0].bar(x_axis, y_axis_negative_values, color="yellow",
                    label='HNN Timely Availability [%],\
 Latency value of infinity')
        axes[0].bar(x_axis, y_axis_below_threshold, color="blue",
                    label='HNN Timely Availability [%],\
 Latency value below threshold')

        legend = axes[0].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="9")
        # Show the grid
        axes[0].set_axisbelow(True)
        axes[0].grid(visible=True, which='both', axis='both', linewidth=0.5)
        axes[0].set_ylim(ymin=90, ymax=100)

        # Second plot
        # Setting up our data
        y_axis_below_threshold = \
            HNE_timely_availability_percentage_dataframe.below_threshold
        y_axis_negative_values = \
            HNE_timely_availability_percentage_dataframe.below_threshold\
            + HNE_timely_availability_percentage_dataframe.negative_value

        axes[1].bar(x_axis, [100], color="red")
        axes[1].bar(x_axis, y_axis_negative_values, color="yellow",
                    label='HNE Timely Availability [%],\
 Latency value of infinity')
        axes[1].bar(x_axis, y_axis_below_threshold, color="blue",
                    label='HNE Timely Availability [%],\
 Latency value below threshold')

        legend = axes[1].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="9")
        axes[1].yaxis.set_major_locator(loc)
        # Show the grid
        axes[1].set_axisbelow(True)
        axes[1].grid(visible=True, which='both', axis='both', linewidth=0.5)
        axes[1].set_ylim(ymin=90, ymax=100)

        # Third plot
        # Setting up our data
        y_axis_below_threshold = \
            HNZ_timely_availability_percentage_dataframe.below_threshold
        y_axis_negative_values = \
            HNZ_timely_availability_percentage_dataframe.below_threshold\
            + HNZ_timely_availability_percentage_dataframe.negative_value

        axes[2].bar(x_axis, [100], color="red")
        axes[2].bar(x_axis, y_axis_negative_values, color="yellow",
                    label='HNZ Timely Availability [%],\
 Latency value of infinity')
        axes[2].bar(x_axis, y_axis_below_threshold, color="blue",
                    label='HNZ Timely Availability [%],\
 Latency value below threshold')
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
    else:
        logging.warning(
            "Skipping Timely Availability. Please double check the latency\
 files")
