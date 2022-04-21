import os

from datetime import date

from pandas.core.frame import DataFrame


def generate_CSV_from_failed_latencies(latencies: DataFrame,
                                       station: str,
                                       network: str,
                                       startdate: date,
                                       enddate: date,
                                       timely_threshold: float
                                       ):
    filename = f'{network}.{station}-{startdate}_to_{enddate}-\
failed_latencies.csv'
    latencies_above_three = latencies.loc[latencies.data_latency
                                          > timely_threshold]
    if 'date' in latencies.columns:
        latencies.drop(
            'date', axis=1, inplace=True)
    latencies_above_three_rounded = latencies_above_three.loc[:,
                                                              ['network',
                                                               'station',
                                                               'channel',
                                                               'startTime',
                                                               'data_latency']]

    latencies_above_three_rounded["data_latency"] = round(
        latencies_above_three_rounded.data_latency.astype(float), 2)

    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    latencies_above_three_rounded.to_csv(
        f'./stationvalidation_output/{filename}', index=False)
