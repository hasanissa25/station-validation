# flake8: noqa
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import numpy as np

register_matplotlib_converters()

# Getting the Data
cn_csv = "tests/generate_ratio_plot/data/CN.A64..HNZ.D.2016-10-21_2016-10-30_PDF.csv"
cn_dataframe = pd.read_csv(cn_csv)
cn_dataframe.sort_values(by='power', ascending=True, inplace=True)
cn_dataframe.drop_duplicates(subset=['frequency'], inplace=True)
cn_dataframe.sort_values(by='frequency', ascending=True, inplace=True)
qw_csv = "tests/generate_ratio_plot/data/QW.QCC02..HNZ.D.2022-03-08_2022-03-17_PDF.csv"
qw_dataframe = pd.read_csv(qw_csv)
qw_dataframe.sort_values(by='power', ascending=True, inplace=True)
qw_dataframe.drop_duplicates(subset=['frequency'], inplace=True)
qw_dataframe.sort_values(by='frequency', ascending=True, inplace=True)


# Setting up the plot
fig = plt.figure()
fig.set_size_inches(18.5, 10.5)
ax1 = fig.add_subplot(111)
ax1 = plt.gca()
# Add a title to the axes.
ax1.set_title("Ratio Plot:\n QW.QCC02 vs CN.A64 (HNZ)")
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Ratio of power')  # Add a y-label to the axes.
# Setting up our data
x_axis = qw_dataframe.frequency
y_axis_cn = cn_dataframe["power"].array
y_axis_qw = qw_dataframe["power"].array

y_axis = []
for index, i in enumerate(y_axis_cn):
    y_axis.append(y_axis_qw[index]/y_axis_cn[index])
# Show the grid
ax1.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
# Plotting the data
ax1.plot(
    x_axis, y_axis,
    marker='o', label='Ratio', linewidth=1, markeredgewidth=1,
    markersize=1, markevery=10, c="green")

fig.tight_layout()  # Important for the plot labels to not overlap

plt.savefig(
    './tests/generate_ratio_plot/QCC02vsA64')
plt.close()
