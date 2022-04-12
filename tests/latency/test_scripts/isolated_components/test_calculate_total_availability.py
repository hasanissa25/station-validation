# flake8: noqa
import json
import math


def calculate_total_availability(files: list):

    total_sum_of_percent_availability = 0.
    length_of_latency_files = len(files)
    total_availability_percentage = 0.

    for file in files:
        json_latency_file = open(file)
        latency_dict = json.load(json_latency_file)

        latency_array = latency_dict["availability"][0]["intervals"]
        length_of_latency_array = len(latency_array)
        local_sum_of_percent_availability = 0
        for latency_value in latency_array:
            local_sum_of_percent_availability += latency_value["percentAvailability"]
        total_sum_of_percent_availability += local_sum_of_percent_availability / \
            length_of_latency_array
    total_availability_percentage = math.floor(
        total_sum_of_percent_availability / length_of_latency_files * 10 ** 2) / 10 ** 2
    return total_availability_percentage
