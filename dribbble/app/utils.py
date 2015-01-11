import os
import requests
import urllib2
import struct

from datetime import datetime, date
from flask import current_app as app
from dateutil.relativedelta import relativedelta

from app.shots.colours import ColorSwatch


def get_shots_by_year():
    shots = []
    urls = get_shot_urls()
    for url in urls:
        shots.append({
            'date': url.get('date'),
            'shots': requests.get(url.get('url')).json()
        })
    return shots


def get_url(path, params=[]):
    access_token = app.config.get('CLIENT_ACCESS_TOKEN')
    base_uri = app.config.get('BASE_URI')
    params.append('access_token=%s' % access_token)
    return '{base_uri}/{path}?{params}'.format(
        base_uri=base_uri, path=path, params='&'.join(params))


def get_shot_urls():
    urls = []
    base_uri = app.config.get('BASE_URI')
    for current_date in get_all_dates():
        params = [
            'per_page=5',
            'date=%s' % current_date.strftime('%Y-%m-%d'),
            'access_token=%s' % app.config.get('CLIENT_ACCESS_TOKEN')
        ]
        url = '{base_uri}/shots?{params}'.format(
            base_uri=base_uri, params='&'.join(params))
        urls.append({
            'date': current_date,
            'url': url
        })
    return urls


def get_all_dates():
    start_date = datetime.strptime('2013-07-29', '%Y-%m-%d')
    current_date = date.today() - relativedelta(days=1)
    dates = [current_date]
    while current_date > start_date.date():
        current_date = current_date - relativedelta(years=1)
        dates.append(current_date)
    return dates


def colour_palette(shot_id):
    aco_file = '%s/%s.aco' % (app.config.get('COLOUR_PALETTE_DIR'), shot_id)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(current_dir, aco_file)):
        download_aco_file(shot_id=shot_id)
        return unpack_aco_file(shot_id=shot_id)


def download_aco_file(shot_id):
    url = app.config.get('COLOUR_PALETTE_URL') % shot_id
    aco_file = urllib2.urlopen(url)
    aco_filename = '%s/%s.aco' % (app.config.get('COLOUR_PALETTE_DIR'), shot_id)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    output = open(os.path.join(current_dir, aco_filename), 'wb')
    output.write(aco_file.read())
    output.close()


def unpack_aco_file(shot_id):
    aco_file_location = '%s/%s.aco' % (
        app.config.get('COLOUR_PALETTE_DIR'), shot_id)
    with open(aco_file_location, "rb") as acoFile:
        version, size, offset, start = 1, 2, 10, 1
        #  skip ver 1 file
        head = acoFile.read(size)
        ver, = struct.unpack(">H", head)
        if (ver != version):
            raise TypeError("Probably not a adobe aco file")
        count = acoFile.read(size)
        cnt, = struct.unpack(">H", count)
        acoFile.seek(cnt * offset, start)

        version = 2
        #  read ver2 file
        head = acoFile.read(size)
        ver, = struct.unpack(">H", head)
        if (ver != version):
            raise TypeError("Probably not a adobe aco file")
        count = acoFile.read(size)
        count, = struct.unpack(">H", count)
        for _ in range(count):
            swatch = ColorSwatch(acoFile)
            import ipdb; ipdb.set_trace()
            print(str(swatch))
