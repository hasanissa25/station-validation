import json
from typing import Tuple

import pandas as pd
from pandas.core.frame import DataFrame


def calculate_apollo_latencies(files: list,
                               network: str,
                               station: str) -> Tuple[DataFrame, list]:
    # Dataframe used to hold latency information for the station
    columns = ('network', 'station', 'channel',
               'startTime', 'data_latency')
    # Storing the data of all the latency files
    combined_latency_data_for_all_days: dict = {}
    # Storing the data of all the latency files seperated into days
    array_of_daily_latency_dataframes = []
    for file in files:
        # Opening JSON file
        json_latency_file = open(file)
        # returns JSON object as a dictionary
        latency_data = json.load(json_latency_file)
        # Storing the data of the current days JSON latency file
        current_day_latency_data: dict = {}
        # Iterating through the json availability array which a string "id",
        # and an array of latency data "Intervals"
        for current_NSC in latency_data['availability']:
            current_id = current_NSC["id"]
            network_station = [network, station]

            # making sure we are looping over the required network station
            # combo, as the current iteration of the latency JSON files,
            # contained all the network and stations in one JSON file
            # for that specific day.
            if all(x in current_id for x in network_station):
                # splitting the id column and fetching the network, station
                # and channel values, id originally looks like the following :
                # "QW.QCC01.HNN"
                current_network, current_station, current_channel = \
                    current_NSC['id'].split(
                        '.')
                # looping over the intervals array, which contains all the
                # latency objects a specific NSC
                for current_latency in current_NSC['intervals']:
                    combined_latency_data_for_all_days, \
                        current_day_latency_data = \
                        get_latency_value_for_current_timestamp(
                            current_latency=current_latency,
                            combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                            current_day_latency_data=current_day_latency_data,
                            current_network=current_network,
                            current_station=current_station,
                            current_channel=current_channel)
        json_latency_file.close()
        daily_latency_dataframe = pd.DataFrame(
            data=current_day_latency_data, index=columns).T
        array_of_daily_latency_dataframes.append(
            daily_latency_dataframe)
    combined_latency_dataframe_for_all_days_dataframe = pd.DataFrame(
        data=combined_latency_data_for_all_days, index=columns).T
    return combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes


def append_to_latency_objects(
        current_latency: float,
        combined_latency_data_for_all_days: dict,
        current_day_latency_data: dict,
        current_network: str,
        current_station: str,
        current_channel: str,
        start_time: str,
        packet_id: str) -> Tuple[dict, dict]:
    combined_latency_data_for_all_days[current_network +
                                       "."+current_station
                                       +
                                       "."+current_channel
                                       +
                                       "." + start_time
                                       +
                                       "." + packet_id] = {'network':
                                                           current_network,
                                                           'station':
                                                           current_station,
                                                           'channel':
                                                               current_channel,
                                                           'startTime':
                                                               start_time,
                                                           'data_latency':
                                                               current_latency
                                                           }
    current_day_latency_data[current_network +
                             "."+current_station +
                             "."+current_channel +
                             "." +
                             start_time +
                             "." + packet_id] = {'network': current_network,
                                                 'station': current_station,
                                                 'channel': current_channel,
                                                 'startTime': start_time,
                                                 'data_latency':
                                                 current_latency
                                                 }
    return combined_latency_data_for_all_days, current_day_latency_data


def get_latency_value_for_current_timestamp(current_latency: dict,
                                            combined_latency_data_for_all_days:
                                            dict,
                                            current_day_latency_data: dict,
                                            current_network: str,
                                            current_station: str,
                                            current_channel: str) -> \
        Tuple[dict, dict]:
    if current_latency["retx"]["allPackets"] == 1:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")
    elif current_latency["retx"]["allPackets"] == 2:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minium"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["minium"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")
    elif current_latency["retx"]["allPackets"] == 3:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minium"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["minium"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")
        if current_latency["latency"]["average"] != -1:
            calculated_unkown_latency_value = (
                3 * current_latency["latency"]["average"]) - \
                current_latency["latency"]["minium"] - \
                current_latency["latency"]["maximum"]
            append_to_latency_objects(
                current_latency=calculated_unkown_latency_value,
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="average")
    elif current_latency["retx"]["allPackets"] > 3:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minium"] != -1:
            append_to_latency_objects(
                current_latency=current_latency["latency"]["minium"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_latency_data=current_day_latency_data,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")
        if current_latency["latency"]["average"] != -1:
            number_of_times_to_append_to_latencies = \
                current_latency["retx"]["allPackets"] - 2
            for iteration in range(number_of_times_to_append_to_latencies):
                append_to_latency_objects(
                    current_latency=current_latency["latency"]["average"],
                    combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                    current_day_latency_data=current_day_latency_data,
                    current_network=current_network,
                    current_station=current_station,
                    current_channel=current_channel,
                    start_time=current_latency[
                        'startTime'],
                    packet_id=f"{iteration}")

    return combined_latency_data_for_all_days, current_day_latency_data
