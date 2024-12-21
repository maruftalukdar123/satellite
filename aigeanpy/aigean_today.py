from argparse import ArgumentParser
from requests import get
from datetime import datetime
import aigeanpy.net as net
from aigeanpy.satmap import SatMap, get_satmap
import sys


def aigean_today(instrument, saveplot):
    '''Download the latest todays image from any of the instruments.
    If saveplot is passed, then saves the PNG created by SatMap.visualize

    Parameters
    ----------
    instrument : str
        The instrument whose latest todays image to download. Must be one of
        lir, manannan, fand or ecne (case insensitive)

    saveplot : Boolean
        True to save a PNG created by passing the downloaded file into
        SatMap.visualize
    '''

    if instrument and instrument not in ['lir','manannan','fand','ecne']:
        sys.exit("-i (--instrument) must be a string and be one of one of 'lir', 'manannan', 'fand' or 'ecne'. Note: instruments are case sensitive")


    date_today = datetime.today().strftime('%Y-%m-%d')
    payload = {'start_date':date_today , 'stop_date':date_today, 'instrument':instrument}
    r = get('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query',params=payload).json()

    if not r:
        sys.exit("There seems to be no observations made today")

    date_time = [[i['date'] + ' ' +i['time']] for i in r]
    date_time = [datetime.strptime(i[0],'%Y-%m-%d %H:%M:%S') for i in date_time]


    latest = r[date_time.index(max(date_time))]
    latest_filename = latest['filename']
    net.download_isa(latest_filename)

    if saveplot:
        if instrument != 'ecne':
            lates_satmap_object = get_satmap(latest_filename)
            lates_satmap_object.visualize(save=True)
        else:
            sys.exit("The file downloaded can not be visualised.")


def cli():
    '''Creates command line interface that calls on the aigean_today function.
    '''

    parser = ArgumentParser(description="Download the lates image from the ISA archives")
    parser.add_argument('-i', '--instrument', type=str, help='The instrument whose image to download')
    parser.add_argument('-s', '--saveplot', action='store_true', help='Set to True to save the picture as a PGN')

    arguments = parser.parse_args()

    aigean_today(arguments.instrument, arguments.saveplot)

if __name__ == '__main__':
    cli()