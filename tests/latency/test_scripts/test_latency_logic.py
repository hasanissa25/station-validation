# type: ignore
# flake8: noqa

# This script is to test our latency generating logic, from fetching the files, to producing the plots
from datetime import date
from stationverification.utilities.latency import getfiles, getlatencies, latency_log_plot, latency_line_plot, generate_CSV_from_failed_latencies, timely_availability_plot, populate_json_with_latency_info
from tests.latency.test_scripts.isolated_components.test_latency_from_CSV import test_latency_from_CSV
from tests.latency.test_scripts.isolated_components.test_get_latencies_from_JSON import test_latency_from_json
import os
import json
# Apollo Parameters
required_network = "QW"
required_station = "QCC02"
typeofinstrument = 'APOLLO'
path = 'tests/data/apollo/archive/latency'
startdate = date(2022, 3, 28)
enddate = date(2022, 3, 29)
timely_threshold = 3
json_dict = {
    "channels": {
        "HNN": {},
        "HNE": {},
        "HNZ": {}
    }}
# Guralp Parameters
# required_network = "QW"
# required_station = "QCN08"
# typeofinstrument = 'GURALP'
# path = 'tests/data/guralp/archive/latency'
# startdate = date(2022, 3, 17)
# enddate = date(2022, 3, 23)

# Returns the file paths containing the latencies in the validation period for the required network and station
files = getfiles(typeofinstrument=typeofinstrument,
                 network=required_network,
                 station=required_station,
                 path=path,
                 startdate=startdate,
                 enddate=enddate)
# Returns the latency handling both Guralp and Apollo
combined_latency_dataframe_for_all_days, array_of_daily_latency_dataframes = getlatencies(
    typeofinstrument=typeofinstrument,
    files=files,
    network=required_network,
    station=required_station,
    startdate=startdate,
    enddate=enddate)

number_of_validation_period_days = len(array_of_daily_latency_dataframes)

generate_CSV_from_failed_latencies(latencies=combined_latency_dataframe_for_all_days,
                                   station=required_station,
                                   network=required_network,
                                   startdate=startdate,
                                   enddate=enddate,
                                   timely_threshold=timely_threshold)

# timely_availability_plot(latencies=array_of_daily_latency_dataframes,
#                          station=required_station,
#                          startdate=startdate,
#                          enddate=enddate,
#                          network=required_network,
#                          timely_threshold=timely_threshold
#                          )

# latency_log_plot(latencies=combined_latency_dataframe_for_all_days,
#                  station=required_station,
#                  startdate=startdate,
#                  enddate=enddate,
#                  typeofinstrument=typeofinstrument,
#                  network=required_network,
#                  number_of_days=number_of_validation_period_days,
#                  timely_threshold=timely_threshold
#                  )


# latency_line_plot(latencies=array_of_daily_latency_dataframes,
#                   station=required_station,
#                   startdate=startdate,
#                   enddate=enddate,
#                   typeofinstrument=typeofinstrument,
#                   network=required_network,
#                   timely_threshold=timely_threshold
#                   )

# json_of_latency = populate_json_with_latency_info(
#     json_dict=json_dict,
#     combined_latency_dataframe_for_all_days=combined_latency_dataframe_for_all_days,
#     network=required_network,
#     station=required_station,
#     timely_threshold=3,
#     timely_percent=97
# )
# if not os.path.isdir('./station_validation_results/'):
#     os.mkdir('./station_validation_results/')
# with open('./station_validation_results/json_report.json', 'w+') as file:
#     json.dump(json_dict, file, indent=2)
