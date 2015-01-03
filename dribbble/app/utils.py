import requests

from datetime import datetime, date
from flask import current_app as app
from dateutil.relativedelta import relativedelta


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
    current_date = date.today()
    dates = [current_date]
    while current_date > start_date.date():
        current_date = current_date - relativedelta(years=1)
        dates.append(current_date)
    return dates
