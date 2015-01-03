from datetime import datetime, date
from flask import current_app as app
from dateutil.relativedelta import relativedelta


def get_url(path, params=[]):
    access_token = app.config.get('CLIENT_ACCESS_TOKEN')
    base_uri = app.config.get('BASE_URI')
    params.append('access_token=%s' % access_token)
    return '{base_uri}/{path}?{params}'.format(
        base_uri=base_uri, path=path, params='&'.join(params))


def get_shot_urls():
    urls = []
    dates = get_all_dates()
    base_uri = app.config.get('BASE_URI')
    for date in dates:
        params = [
            'per_page=15',
            'date=%s' % date.strftime('%Y-%m-%d'),
            'access_token=%s' % app.config.get('CLIENT_ACCESS_TOKEN')
        ]
        urls.append(
            '{base_uri}/shots?{params}'.format(
                base_uri=base_uri, path=path, params='&'.join(params)))
    return urls


def get_all_dates():
    start_date = datetime.strptime('2009-07-29')
    year = date.today().year
    return datetime.now() - relativedelta(years=number_of_years)
