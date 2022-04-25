import os
import numpy as np
from datetime import date, timedelta
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker


def plot_timing_quality(network: str,
                        station: str,
                        startdate: date,
                        enddate: date,
                        results: Any,
                        threshold: float):

    # Generatre x-axis values as days since startdate
    difference = enddate - startdate
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim(ymin=50, ymax=100)
    size_of_x_axis = x_axis.size
    size_of_metric_data = len(results)
    if size_of_metric_data == size_of_x_axis:
        ax.bar(x_axis, [100], color="red")
        ax.bar(
            x_axis, results)

        def timeTicks(x, pos):
            date = startdate + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)
        filename = ""
        if startdate == enddate - timedelta(days=1):
            filename = f'{network}.{station}.{startdate}'
        else:
            filename = f'{network}.{station}-{startdate}_to_\
{enddate - timedelta(days=1)}'
        ax.set_title(
            f'Timing Quality [%]\n{filename}')
        plt.ylabel('Timing Quality')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Adding the threshold line
        ax.axhline(threshold, color='r', linewidth="1", linestyle='--',
                   label=f'Timing Quality Threshold: {threshold}%')
        # Adding the legend
        legend = ax.legend(bbox_to_anchor=(1, 1),
                           loc='upper right', fontsize="9")
        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        # Write the plot to the output directory
        if not os.path.isdir("./stationvalidation_output"):
            os.mkdir('./stationvalidation_output')
        # plt.savefig(f'stationvalidation_output/{plot_filename}')
        plt.savefig(f'stationvalidation_output/{filename}-timing_quality.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        plt.close()