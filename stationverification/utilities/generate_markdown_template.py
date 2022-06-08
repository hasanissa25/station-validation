# flake8: noqa
from jinja2 import Template
from stationverification.utilities.GitLabAttachments import Attachments

def generate_markdown_template(attachments: Attachments) -> str:

    template = Template('''
<details><summary>JSON Report</summary>
{% for element in validation_results -%}
    {{ element["link"] }}
{% endfor %}
</details>

<details><summary>PDF</summary>
{% for element in pdf -%}
 {{ element["link"] }}
{% endfor %}
</details>

<details><summary>Latency Log Plot</summary>
{% for element in latency_log_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Latency Line Plots</summary>
{% for element in latency_line_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Failed Latencies</summary>
{% for element in failed_latencies -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timely Availability</summary>
{% for element in timely_availability_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timing Error</summary>
{% for element in timing_error -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timing Quality</summary>
{% for element in timing_quality -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>ADC Count</summary>
{% for element in adc_count -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Max Gap</summary>
{% for element in max_gap -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Gaps</summary>
{% for element in num_gaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Overlaps</summary>
{% for element in num_overlaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Spikes</summary>
{% for element in spikes -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent Availability</summary>
{% for element in percent_availability -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent above New High Noise Model</summary>
{% for element in pct_above_nhnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent below New Low Noise Model</summary>
{% for element in pct_below_nlnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
''')
    template_render = template.render(
        failed_latencies=attachments.failed_latencies,
        latency_line_plot=attachments.latency_line_plot,
        latency_log_plot=attachments.latency_log_plot,
        timely_availability_plot=attachments.timely_availability_plot,
        timing_error=attachments.timing_error,
        timing_quality=attachments.timing_quality,
        validation_results=attachments.validation_results,
        adc_count=attachments.adc_count,
        max_gap=attachments.max_gap,
        num_gaps=attachments.num_gaps,
        num_overlaps=attachments.num_overlaps,
        pct_above_nhnm=attachments.pct_above_nhnm,
        pct_below_nlnm=attachments.pct_below_nlnm,
        percent_availability=attachments.percent_availability,
        spikes=attachments.spikes,
        pdf=attachments.pdf,
    )
    return template_render
