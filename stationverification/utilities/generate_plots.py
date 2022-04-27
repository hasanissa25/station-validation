'''
This module generates plots to be used in the station verification process

Functions
---------

plot_psd:
    Plots probabilistic spectral density data against the 2g and 4g noise
    curves

ADC_plot:
    Plots the sample min, max, mean and median so that symetry can be visually
    verified

max_gap_plot:
    Plots the max gap metric returned from ispaq
num_gaps_plot:
    Plots the num_gaps metric returned from ispaq
num_overlaps_plot:
    Plots the num_overlaps metric returned from ispaq
spikes_plot:
    Plots the spikes metric returned from ispaq
percent_availability_plot:
    Plots the percent_availability metric returned from ispaq
pct_above_nhnm_plot:
    Plots the pct_above_nhnm metric returned from ispaq
pct_below_nlnm_plot:
    Plots the pct_below_nlnm metric returned from ispaq
dead_channel_lin_plot:
    Plots the dead_channel_lin metric returned from ispaq
dead_channel_gsn_plot:
    Plots the dead_channel_gsn metric returned from ispaq

'''
import logging
import os
from datetime import date, timedelta
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker


from .generate_report import StationMetricData


class PlotParameters(dict):
    @property
    def network(self) -> str:
        return self["network"]

    @property
    def station(self) -> str:
        return self["station"]

    @property
    def stationMetricData(self) -> StationMetricData:
        return self["stationMetricData"]

    @property
    def start(self) -> date:
        return self["start"]

    @property
    def stop(self) -> date:
        return self["stop"]

    @property
    def channel(self) -> str:
        return self["channel"]


def plot_metrics(plotParameters: PlotParameters):
    if not os.path.isdir("./stationvalidation_output"):
        os.mkdir('./stationvalidation_output')
    ADC_plot(plotParameters)
    max_gap_plot(plotParameters)
    num_gaps_plot(plotParameters)
    num_overlaps_plot(plotParameters)

    spikes_plot(plotParameters)
    percent_availability_plot(plotParameters)
    pct_above_nhnm_plot(plotParameters)
    pct_below_nlnm_plot(plotParameters)

    # dead_channel_lin_plot(plotParameters)
    # dead_channel_gsn_plot(plotParameters)

# Function to graph the ADC plot for visual representation
# Since what values are normal for these metrics seems to differ from one
# channel to the next, it was difficult to come up with thresholds. However,
# according to IRIS documentation, the sample_min and sample_max should be
# roughly symmetrical around sample_mean and sample_median. I thought a good
# way to represent this would be to generate a plot of these values


def ADC_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    ax = plt.gca()

    # Plot the min, max and median normalized to the mean. This makes it
    # easier to see how symmetrical it is.
    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'sample_max', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_max', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: max deviation from mean')
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_min', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: min deviation from mean')
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_median', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: median deviation from mean')
        ax.scatter(
            x_axis, stationMetricData.get_values(
                'sample_rms', network, station, channel),
            marker='o', label='Sample RMS')

        legend = plt.legend(fancybox=True, framealpha=0.2,
                            bbox_to_anchor=(1.4, 1.0),
                            loc='upper right', fontsize="9")
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)
        plt.title(
            f'{network}.{station}.{channel} - \
ADC Count (range: [0, +/- 8,388,608])')
        plt.ylabel('Amplitude value')
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}.ADC_Count'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.ADC_Count'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300,
                    bbox_extra_artists=(legend,),
                    bbox_inches='tight')
    plt.close()


def num_overlaps_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    # loc = plticker.MultipleLocator(base=1.0)
    # ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'num_overlaps', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'num_overlaps', network, station, channel))
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(f'{network}.{station}.{channel} - Number of overlaps')
        plt.ylabel('Overlaps')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}\
.num_overlaps'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.num_overlaps'

        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def num_gaps_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    # loc = plticker.MultipleLocator(base=1.0)
    # ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'num_gaps', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'num_gaps', network, station, channel))

        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(f'{network}.{station}.{channel} - Number of Gaps')
        plt.ylabel('Gaps')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}.num_gaps'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.num_gaps'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def max_gap_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    # loc = plticker.MultipleLocator(base=1.0)
    # ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'max_gap', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'max_gap', network, station, channel))
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(f'{network}.{station}.{channel} - Max Gaps')
        plt.ylabel('Gap size')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}.max_gap'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.max_gap'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def spikes_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    # loc = plticker.MultipleLocator(base=1.0)
    # ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'spikes', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'spikes', network, station, channel))

        # legend = plt.legend(fancybox=True, framealpha=0.2,
        #                     loc='upper right', fontsize="9")
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(f'{network}.{station}.{channel} - Spikes')
        plt.ylabel('Spikes')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}.spikes'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.spikes'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def percent_availability_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'percent_availability', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(x_axis, [100], color="red")
        ax.bar(
            x_axis, stationMetricData.get_values(
                'percent_availability', network, station, channel))

        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(f'{network}.{station}.{channel} - Percent Availability')
        plt.ylabel('Availability')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        ax.set_ylim(ymin=90, ymax=100)
        # this locator puts ticks at regular intervals in setps of "base"
        loc = plticker.MultipleLocator(base=2)
        ax.yaxis.set_major_locator(loc)
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}\
.percent_availability'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.percent_availability'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def pct_above_nhnm_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'pct_above_nhnm', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'pct_above_nhnm', network, station, channel))

        # legend = plt.legend(fancybox=True, framealpha=0.2,
        #                     loc='upper right', fontsize="9")
        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(
            f'{network}.{station}.{channel} - \
Percent above New High Noise Model')
        plt.ylabel('Percentage')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}\
.pct_above_nhnm'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.pct_above_nhnm'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def pct_below_nlnm_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'pct_below_nlnm', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.bar(
            x_axis, stationMetricData.get_values(
                'pct_below_nlnm', network, station, channel))

        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)

        ax.set_title(
            f'{network}.{station}.{channel} - \
Percent below New Low Noise Model')
        plt.ylabel('Percentage')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{network}.{station}.{channel}.{start}\
.pct_below_nlnm'
        else:
            plot_filename = f'{network}.{station}.{channel}.{start}_\
{(stop + timedelta(days=-1))}.pct_below_nlnm'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


# def dead_channel_lin_plot(
#     plotParameters: PlotParameters
# ):
#     network = plotParameters.network
#     station = plotParameters.station
#     channel = plotParameters.channel
#     stationMetricData = plotParameters.stationMetricData
#     start = plotParameters.start
#     stop = plotParameters.stop

#     # Generatre x-axis values as days since startdate
#     difference = stop - start
#     x_axis = np.arange(0, difference.days, 1)

#     # Create plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     # this locator puts ticks at regular intervals in setps of "base"
#     # loc = plticker.MultipleLocator(base=1.0)
#     # ax.yaxis.set_major_locator(loc)

#     size_of_x_axis = x_axis.size
#     size_of_metric_data = len(stationMetricData.get_values(
#         'dead_channel_lin', network, station, channel))
#     if size_of_metric_data == size_of_x_axis:
#         ax.bar(
#             x_axis, stationMetricData.get_values(
#                 'dead_channel_lin', network, station, channel))

#         # Function for formatting the x values to actually be dates

#         def timeTicks(x, pos):
#             date = start + timedelta(days=x)
#             return str(date.isoformat())

#         # Format the x axis values to be dates and rotate them 90 degrees
#         formatter = matplotlib.ticker.FuncFormatter(timeTicks)
#         ax.xaxis.set_major_formatter(formatter)
#         plt.xticks(rotation=90)

#         ax.set_title(f'{network}.{station}.{channel} - Dead Channel Lin')

#         # Add a grid to the plot to make the symmetry more obvious
#         ax.set_axisbelow(True)
#         plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

#         # Save the plot to file and then close it so the next channel's\
#  metrics
#         # aren't plotted on the same plot
#         if start == stop - timedelta(days=1):
#             plot_filename = f'{network}.{station}.{channel}.{start}\
# .dead_channel_lin'
#         else:
#             plot_filename = f'{network}.{station}.{channel}.{start}_\
# {(stop + timedelta(days=-1))}.dead_channel_lin'
#         # Write the plot to the output directory
#         plt.savefig(f'stationvalidation_output/{plot_filename}.png',
#                     dpi=300, bbox_inches='tight')
#         logging.info(f'{plot_filename} created.')
#     plt.close()


# def dead_channel_gsn_plot(
#     plotParameters: PlotParameters
# ):
#     network = plotParameters.network
#     station = plotParameters.station
#     channel = plotParameters.channel
#     stationMetricData = plotParameters.stationMetricData
#     start = plotParameters.start
#     stop = plotParameters.stop

#     # Generatre x-axis values as days since startdate
#     difference = stop - start
#     x_axis = np.arange(0, difference.days, 1)

#     # Create plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     # this locator puts ticks at regular intervals in setps of "base"
#     # loc = plticker.MultipleLocator(base=1.0)
#     # ax.yaxis.set_major_locator(loc)

#     size_of_x_axis = x_axis.size
#     size_of_metric_data = len(stationMetricData.get_values(
#         'dead_channel_gsn', network, station, channel))
#     if size_of_metric_data == size_of_x_axis:
#         ax.bar(
#             x_axis, stationMetricData.get_values(
#                 'dead_channel_gsn', network, station, channel))

#         # Function for formatting the x values to actually be dates

#         def timeTicks(x, pos):
#             date = start + timedelta(days=x)
#             return str(date.isoformat())

#         # Format the x axis values to be dates and rotate them 90 degrees
#         formatter = matplotlib.ticker.FuncFormatter(timeTicks)
#         ax.xaxis.set_major_formatter(formatter)
#         plt.xticks(rotation=90)

#         ax.set_title(f'{network}.{station}.{channel} - Dead Channel GSN')

#         # Add a grid to the plot to make the symmetry more obvious
#         ax.set_axisbelow(True)
#         plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

#         # Save the plot to file and then close it so the next channel's\
#  metrics
#         # aren't plotted on the same plot
#         if start == stop - timedelta(days=1):
#             plot_filename = f'{network}.{station}.{channel}.{start}\
# .dead_channel_gsn'
#         else:
#             plot_filename = f'{network}.{station}.{channel}.{start}_\
# {(stop + timedelta(days=-1))}.dead_channel_gsn'
#         # Write the plot to the output directory
#         plt.savefig(f'stationvalidation_output/{plot_filename}.png',
#                     dpi=300, bbox_inches='tight')
#         logging.info(f'{plot_filename} created.')
#     plt.close()
