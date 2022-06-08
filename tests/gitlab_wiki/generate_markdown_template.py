def generate_markdown_template() -> str:
    return \
        '''
<details><summary>JSON Report</summary>

```json 
{
    "network_code": "QW",
}
```
</details>

<details><summary>PDF</summary>
</details>

<details><summary>Latency Log Plot</summary>

</details>
<details><summary>Latency Line Plots</summary>
</details>
<details><summary>Failed Latencies</summary>

</details>
<details><summary>Timely Availability</summary>

</details>
<details><summary>Timing Error</summary>

</details>
<details><summary>Timing Quality</summary>

</details>
<details><summary>ADC Count</summary>

</details>
<details><summary>Max Gap</summary>

</details>
<details><summary>Number of Gaps</summary>

</details>
<details><summary>Number of Overlaps</summary>

</details>
<details><summary>Spikes</summary>

</details>
<details><summary>Percent Availability</summary>

</details>
<details><summary>Percent above New High Noise Model</summary>

</details>
<details><summary>Percent below New Low Noise Model</summary>

</details>
'''
