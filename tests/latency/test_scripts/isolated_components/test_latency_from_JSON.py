# This script is a testing ground, replacing the getlatencies function from the latency module (Only for testing)
# flake8: noqa
from pandas.core.frame import DataFrame
import pandas as pd
# from matplotlib.ticker import MultipleLocator
from typing import Tuple
import json


def test_latency_from_json(
    typeofinstrument: str,
    files: list,
    network: str,
    station: str
) -> Tuple[DataFrame, list]:
    # Dataframe used to hold latency information for the station
    columns = ('network', 'station', 'channel',
               'startTime', 'data_latency')
    combined_latency_data_for_all_days = {}
    array_of_daily_latency_dataframes = []
    if typeofinstrument == "APOLLO":
        for file in files:
            # Opening JSON file
            json_latency_file = open(file)
            # returns JSON object as a dictionary
            latency_data = json.load(json_latency_file)
            # Storing the data of the current days JSON latency file
            current_day_latency_data = {}
            # Iterating through the json availability array which a string "id", and an array of latency data "Intervals"
            for current_NSC in latency_data['availability']:
                current_id = current_NSC["id"]
                network_station = [network, station]

                # making sure we are looping over the required network station combo, as the current iteration of the latency JSON files,
                # contain all the network and stations in one JSON file for that specific day
                if all(x in current_id for x in network_station):
                    # splitting the id column and fetching the network, station and channel values, id originally looks like the following : "QW.QCC01.HNN"
                    current_network, current_station, current_channel = \
                        current_NSC['id'].split('.')
                    # looping over the intervals array, which contains all the latency objects in 1 second intervals for a specific NSC
                    for current_latency in current_NSC['intervals']:
                        if current_latency["latency"]["maximum"] != -1:
                            # The latency data of all days that we are iterating over
                            combined_latency_data_for_all_days[current_network +
                                                               "."+current_station +
                                                               "."+current_channel +
                                                               "." +
                                                               current_latency['startTime']] = \
                                {'network': current_network,
                                 'station': current_station,
                                 'channel': current_channel,
                                 'startTime': current_latency["startTime"],
                                 'data_latency':
                                 current_latency['latency']['maximum']
                                 }
                            # The latency data of only the current day we are iterating over
                            current_day_latency_data[current_network +
                                                     "."+current_station +
                                                     "."+current_channel +
                                                     "." +
                                                     current_latency['startTime']] = \
                                {'network': current_network,
                                 'station': current_station,
                                 'channel': current_channel,
                                 'startTime': current_latency["startTime"],
                                 'data_latency':
                                 current_latency['latency']['maximum']
                                 }

            json_latency_file.close()

            daily_latency_dataframe = pd.DataFrame(
                data=current_day_latency_data, index=columns).T
            array_of_daily_latency_dataframes.append(
                daily_latency_dataframe)
        combined_latency_dataframe_for_all_days = pd.DataFrame(
            data=combined_latency_data_for_all_days, index=columns).T
    return combined_latency_dataframe_for_all_days, array_of_daily_latency_dataframes
