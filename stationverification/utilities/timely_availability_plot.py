import os
import warnings

import numpy as np
from datetime import date, timedelta

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker

from pandas.core.frame import DataFrame
from pandas.plotting import register_matplotlib_converters

from stationverification.utilities.get_timely_availability_arrays\
    import get_timely_availability_arrays


warnings.filterwarnings("ignore")


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
        filename = f'{network}.{station}-{startdate}\
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
