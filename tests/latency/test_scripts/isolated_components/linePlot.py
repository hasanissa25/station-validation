# Script to test generating line plots
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates

register_matplotlib_converters()

data_to_append = {}
columns = ('network', 'station', 'channel',
           'startTime', 'data_latency')
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:00.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:00.000000000Z",
     'data_latency': 2,
     }
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:02.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:02.000000000Z",
     'data_latency': 2.501298176,
     }
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:04.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:04.000000000Z",
     'data_latency': 2.1,
     }
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:06.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:06.000000000Z",
     'data_latency': 6,
     }
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:08.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:08.000000000Z",
     'data_latency': 2.5,
     }
data_to_append["QW.QCC01.HNN.2022-02-02T00:00:10.000000000Z"] = \
    {'network': "QW",
     'station': "QCC01",
     'channel': "HNN",
     'startTime': "2022-02-02T00:00:10.000000000Z",
     'data_latency': 5,
     }
latency_dataframe = pd.DataFrame(data=data_to_append, index=columns).T

filtered_above_three_latencies = latency_dataframe.loc[(
    latency_dataframe['data_latency'] >= 3)]


# Setting up the plot
fig = plt.figure()
fig.set_size_inches(18.5, 10.5)
ax1 = fig.add_subplot(111)
ax1 = plt.gca()
ax1.set_title("Latency")  # Add a title to the axes.
ax1.set_xlabel('Hours since start date')
ax1.set_ylabel('Latency')  # Add a y-label to the axes.
ax1.set_ylim([0, 10])

# Adding the threshold line
threshold = 3
plt.axhline(threshold, color='r', linestyle='--', linewidth="1")
plt.show()

# Setting up our data
x_axis = latency_dataframe.startTime
x_axis_as_dates = [pd.to_datetime(
    x, infer_datetime_format=True).to_pydatetime() for x in x_axis]
y_axis = latency_dataframe.data_latency

x_axis_above_three = filtered_above_three_latencies.startTime
x_axis_above_three_as_dates = [pd.to_datetime(
    x, infer_datetime_format=True).to_pydatetime() for x in x_axis_above_three]
y_axis_above_three = filtered_above_three_latencies.data_latency


# Format the dates on the x-axis
formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M:%S")
ax1.xaxis.set_major_formatter(formatter)
locator = mdates.HourLocator()
ax1.xaxis.set_major_locator(locator)
ax1.tick_params(axis='x', labelrotation=90)

# Show the grid
ax1.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

# Plotting the data
ax1.plot(
    x_axis_as_dates, y_axis,
    marker='o', label='Latency values', linewidth=1, markeredgewidth=1,
    markersize=1, markevery=10000, c="green")
ax1.scatter(
    x_axis_above_three_as_dates, y_axis_above_three,
    marker='o', label='Latency values', c="red")

fig.tight_layout()  # Important for the plot labels to not overlap

plt.savefig(
    './tests/latency/test_scripts/line-plot')
plt.close()
