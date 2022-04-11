from datetime import date, timedelta
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

start = date(2022, 3, 1)
stop = date(2022, 3, 9)
# Generatre x-axis values as days since startdate
difference = stop - start
x_axis = np.arange(0, difference.days, 1)

ax = plt.gca()
sample_max = [-581662.0, -580937.0, -574318.0, -
              578074.0, -572306.0, -563606.0, 4690880.0, 5291900.0]
sample_mean = [-587366.0, -588072.0, -582005.0, -
               584116.0, -579442.0, -570817.0, -559618.0, -557070.0]
after_subtraction = [5704,  7135,  7687, 6042, 7136, 7211, 4131262, 5848]

ax.scatter(
    x_axis, after_subtraction,
    marker='o', label='ADC Counts: max deviation from mean')
legend = plt.legend(fancybox=True, framealpha=0.2,
                    bbox_to_anchor=(1.4, 1.0),
                    loc='upper right', fontsize="9")


def timeTicks(x, pos):
    date = start + timedelta(days=x)
    return str(date.isoformat())


# Format the x axis values to be dates and rotate them 90 degrees
formatter = matplotlib.ticker.FuncFormatter(timeTicks)
ax.xaxis.set_major_formatter(formatter)
plt.xticks(rotation=90)
plt.title('ADC Count(range: [0, +/- 8, 388, 608])')
plt.ylabel('Amplitude value')
ax.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

plt.savefig('tests/generate_plots/test_script/test_adc.png',
            dpi=300,
            bbox_extra_artists=(legend,),
            bbox_inches='tight')
plt.close()
