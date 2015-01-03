import requests

from flask import Blueprint, render_template
from dribbble import utils

mod = Blueprint('shots', __name__, url_prefix='/shots')


@mod.route('/list/', methods=['GET'])
def list():
    url = utils.get_url(path='shots')
    shots = requests.get(url).json()
    return render_template('shots/list.html', shots=shots)


@mod.route('/years-ago/<int:number_of_years>/', methods=['GET'])
def years_ago(number_of_years):
    date = utils.years_ago(number_of_years)
    params = [
        'per_page=15',
        'date=%s' % date.strftime('%Y-%m-%d')
    ]
    url = utils.get_url(path='shots', params=params)
    shots = requests.get(url).json()
    return render_template('shots/today.html', shots=shots)


@mod.route('/detail/<int:shot_id>/', methods=['GET'])
def detail(shot_id):
    url = utils.get_url(path='shots/%s' % shot_id)
    shot = requests.get(url).json()
    return render_template('shots/detail.html', shot=shot)
