import requests


def main():
    station_url = "http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=response&nodata=404"  # noqa
    request = requests.get(station_url, allow_redirects=True)
    request.raise_for_status()
    open('stationverification/data/QW.xml', 'wb').write(request.content)
