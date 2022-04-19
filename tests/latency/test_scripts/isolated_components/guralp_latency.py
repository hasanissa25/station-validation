# This script is to test fetching latency data from a CSV file
import pandas as pd
from datetime import date, timedelta
import re

# flake8: noqa
startdate = date(2022, 1, 1)
enddate = date(2022, 1, 3)
combined_latency_dataframe_for_all_days = pd.DataFrame(
    {'network': [], 'station': [], 'channel': [], "startTime": [], 'data_latency': []})
array_of_daily_latency_dataframes = []
# current_day_latency_data = {}
current_file_dataframe = pd.read_csv(
    'tests/data/guralp/archive/latency/2022/01/01/QW_QCC01_0J_HNE_2022_001_test.csv')

current_file_dataframe[['network', 'station', "location", 'channel']
                       ] = current_file_dataframe['channel'].str.split('.',
                                                                       expand=True)


current_file_dataframe.rename(columns={"channel": "channel",
                                       "network latency": "network_latency",
                                       "data latency": "data_latency",
                                       "network": "network",
                                       "station": "station",
                                       "location": "location",
                                       "timestamp": "startTime"}, inplace=True)

current_file_dataframe[['data_latency']
             ] = current_file_dataframe['data_latency'].str.extract('=(.*)/').astype(float)/100  # noqa: E501
current_file_dataframe['data_latency'] = current_file_dataframe['network_latency'] + \
    current_file_dataframe['data_latency']
print("current_file_dataframe\n", current_file_dataframe)
# list_of_split_data_latency = re.split(
#     "[+\/]", current_data_latency.replace("=", ""))
# current_file_dataframe["data_latency"] = \
#     float(list_of_split_data_latency[0]) / \
#     float(list_of_split_data_latency[1]) + \
#     float(list_of_split_data_latency[2])

# combined_latency_dataframe_for_all_days = combined_latency_dataframe_for_all_days.append(
#         current_file_dataframe[['network', 'station', 'channel', 'startTime', 'data_latency']], sort=False)  # noqa: E501
