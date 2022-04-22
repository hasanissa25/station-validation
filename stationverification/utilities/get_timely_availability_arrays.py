from typing import Tuple
from pandas.core.frame import DataFrame


def get_timely_availability_arrays(
    latencies: DataFrame, threshold: float
) -> Tuple[list, list, list]:
    HNN_timely_availability_percentage_array = []
    HNE_timely_availability_percentage_array = []
    HNZ_timely_availability_percentage_array = []

    for latency_dataframe in latencies:
        HNN_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNN"]
        total_number_of_HNN_latencies = HNN_latencies["data_latency"].size
        number_of_HNN_latencies_below_threshold =\
            HNN_latencies.loc[HNN_latencies["data_latency"]
                              <= threshold]["data_latency"].size
        HNN_timely_availability_percentage_array.append(round(float(
            number_of_HNN_latencies_below_threshold /
            total_number_of_HNN_latencies * 100), 2))

        HNE_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNE"]

        total_number_of_HNE_latencies = HNE_latencies["data_latency"].size
        number_of_HNE_latencies_below_threshold =\
            HNE_latencies.loc[HNE_latencies["data_latency"]
                              <= threshold]["data_latency"].size
        HNE_timely_availability_percentage_array.append(round(float(
            number_of_HNE_latencies_below_threshold /
            total_number_of_HNE_latencies * 100), 2))
        HNZ_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                          "HNZ"]
        total_number_of_HNZ_latencies = HNZ_latencies["data_latency"].size
        number_of_HNZ_latencies_below_threshold =\
            HNZ_latencies.loc[HNZ_latencies["data_latency"]
                              <= threshold]["data_latency"].size
        HNZ_timely_availability_percentage_array.append(round(float(
            number_of_HNZ_latencies_below_threshold /
            total_number_of_HNZ_latencies * 100), 2))
    return HNN_timely_availability_percentage_array,\
        HNE_timely_availability_percentage_array, \
        HNZ_timely_availability_percentage_array
