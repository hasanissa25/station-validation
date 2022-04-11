# Script to test generating log plots

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

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

bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
        5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
# Setting up the plot
fig = plt.figure()
fig.set_size_inches(18.5, 10.5)
ax1 = fig.add_subplot(111)
ax1 = plt.gca()
ax1.set_title("Latency")  # Add a title to the axes.
ax1.set_xlabel('Latency')
ax1.set_ylabel('Occurences')  # Add a y-label to the axes.
ax1.set_yscale('log')
apollo_expected_total_number_of_packets = 13


data_availability = f'{round(float(latency_dataframe.data_latency.size / apollo_expected_total_number_of_packets * 100), 2)}%'  # noqa
note_content = f'Instrument: Apollo\n\
Actual number of data points: {latency_dataframe.data_latency.size}\n\
Expected number of data points: {apollo_expected_total_number_of_packets}\
\nData availability: {data_availability}'
ax1.text(0, 1, note_content, style='italic', fontsize=9,
         transform=ax1.transAxes,
         bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 6})
# Show the grid
ax1.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

# Plotting the data
ax1.hist(latency_dataframe.data_latency, ec='black', bins=bins)
# For the minor ticks, use no labels; default NullFormatter.
ax1.xaxis.set_minor_locator(MultipleLocator(1))

# Adding the threshold line
threshold = 3
plt.axvline(threshold, color='r', linestyle='--', linewidth=1)
plt.show()

fig.tight_layout()  # Important for the plot labels to not overlap

plt.savefig(
    './tests/latency/test_scripts/log-plot')
plt.close()
