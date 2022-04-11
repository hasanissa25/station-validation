import os
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Create plot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.bar(
    [1, 2, 3], [1, 2, 8])

# this locator puts ticks at regular intervals 0-100
loc = plticker.MultipleLocator(base=1.0)
ax.yaxis.set_major_locator(loc)

ax.set_title("Number of overlaps")
plt.ylabel('Overlaps')
ax.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
# Write the plot to the output directory
if not os.path.isdir("tests/generate_plots/test_script"):
    os.mkdir('tests/generate_plots/test_script')
# plt.savefig(f'station_validation_results/{plot_filename}')
plt.savefig('tests/generate_plots/test_script/testPlot.png',
            dpi=300,
            bbox_inches='tight')
plt.close()
