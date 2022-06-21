import requests


def main():
    station_url = "http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=channel&nodata=404"  # noqa
    request = requests.get(station_url, allow_redirects=True)
    open('stationverification/data/QW.xml', 'wb').write(request.content)
