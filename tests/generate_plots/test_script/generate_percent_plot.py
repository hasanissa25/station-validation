
from datetime import date, timedelta
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker

fig, axes = plt.subplots(
    3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False,
                bottom=False, left=False, right=False)
plt.title(
    'Timely Availability [%]')
axes[1].set_ylabel("Timely availability [%]")

enddate = date(2022, 3, 18)
startdate = date(2022, 3, 8)

# Setting up our X-axis data
difference = enddate - startdate
x_axis = np.arange(0, difference.days, 1)

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
y_axis = [95, 100, 98, 96, 97, 95, 100, 98, 96, 97]
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
y_axis = [95, 100, 98, 96, 97, 95, 100, 98, 96, 97]
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
y_axis = [95, 100, 98, 96, 97, 95, 100, 98, 96, 97]
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

plt.savefig(
    'tests/generate_plots/test_script/test_plot',
    bbox_extra_artists=(legend,),
    bbox_inches='tight')
plt.close()
