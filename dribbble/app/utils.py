from datetime import datetime, date
from flask import current_app as app
from dateutil.relativedelta import relativedelta


def get_shots():
    shots = []
    for url in urls:
        shots.append(requests.get(url).json())
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
            'per_page=15',
            'date=%s' % current_date.strftime('%Y-%m-%d'),
            'access_token=%s' % app.config.get('CLIENT_ACCESS_TOKEN')
        ]
        urls.append(
            '{base_uri}/shots?{params}'.format(
                base_uri=base_uri, path=path, params='&'.join(params)))
    return urls


def get_all_dates():
    start_date = datetime.strptime('2009-07-29', '%Y-%m-%d')
    current_date = date.today()
    dates = []
    while current_date > start_date:
        dates.append(current_date)
        current_date = current_date - relativedelta(years=1)
    return dates
