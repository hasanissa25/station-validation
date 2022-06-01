import os
import arrow

import numpy as np
from datetime import date, timedelta
from typing import Any
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.dates as mdates


def plot_clock_offset(network: str,
                      station: str,
                      startdate: date,
                      enddate: date,
                      clock_offset_results: Any,
                      clock_locked_results: Any,
                      threshold: float):

    filename = ""
    if startdate == enddate - timedelta(days=1):
        filename = f'{network}.{station}...{startdate}'
    else:
        filename = f'{network}.{station}...{startdate}_\
{enddate - timedelta(days=1)}'

    # Setting up the figure
    fig, axes = plt.subplots(
        2, 1, sharex=True, sharey=False, figsize=(18.5, 10.5))
    font = {'size': 13}

    matplotlib.rc('font', **font)
    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)

    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', which='both', top=False,
                    bottom=False, left=False, right=False)
    plt.title(
        f'Timing Error (+/- 0.5 microseconds rounded to 0)\n{filename}')

    # Generatre x-axis values as days since startdate
    difference = enddate - startdate
    x_axis = np.arange(0, difference.days, 1)
    x_axis_as_dates = [
        arrow.get(startdate + timedelta(days=float(x))).datetime
        for x in x_axis]
    # this locator puts ticks at regular intervals in steps of "base"
    loc = plticker.MultipleLocator(base=0.5)
    axes[0].yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    if len(clock_offset_results) == size_of_x_axis and\
            size_of_x_axis == len(clock_locked_results):
        # First Plot
        axes[0].scatter(
            x_axis_as_dates, clock_offset_results)
        axes[0].set_ylabel('Timing Error (microseconds)')
        # Format the axis values
        formatter = mdates.DateFormatter("%Y-%m-%d")
        axes[0].xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        axes[0].xaxis.set_major_locator(locator)
        axes[0].tick_params(axis='x', labelrotation=90)
        axes[0].set_ylim(ymin=-2, ymax=2)

        # Add a grid to the plot to make the symmetry more obvious
        axes[0].set_axisbelow(True)
        axes[0].grid(visible=True, which='both',
                     axis='both', linewidth=0.5)

        # Adding the threshold line
        axes[0].axhline(threshold, color='r', linewidth="1", linestyle='--',
                        label=f'Timing Error Thresholds: \
    +/- {threshold} microseconds')
        axes[0].axhline(-threshold, color='r', linewidth="1", linestyle='--')
        # Adding the legend
        legend = axes[0].legend(bbox_to_anchor=(1, 1),
                                loc='upper right', fontsize="9")

        # Second Plot
        axes[1].scatter(
            x_axis_as_dates, clock_locked_results,
            label='0 = Clock is Off\n1 = Clock is Unlocked\n2 \
= Clock is Locked')
        # Add a y-label to the axes.
        axes[1].set_ylabel('Clock Status')
# labelpad=20
        axes[1].set_ylim(ymin=-1, ymax=3)

        # Add a grid to the plot to make the symmetry more obvious
        axes[1].set_axisbelow(True)
        axes[1].grid(visible=True, which='both',
                     axis='both', linewidth=0.5)
        # this locator puts ticks at regular intervals in steps of "base"
        loc = plticker.MultipleLocator(base=1)
        axes[1].yaxis.set_major_locator(loc)
        # Adding the legend
        legend = axes[1].legend(bbox_to_anchor=(1, 1),
                                loc='upper right', fontsize="9")
        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        # Write the plot to the output directory
        if not os.path.isdir("./stationvalidation_output"):
            os.mkdir('./stationvalidation_output')
        plt.savefig(f'stationvalidation_output/{filename}.timing_error.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        plt.close()
