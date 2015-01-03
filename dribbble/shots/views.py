import requests

from flask import Blueprint, render_template, request
from dribbble import utils

mod = Blueprint('shots', __name__, url_prefix='/shots')



@mod.route('/list/', methods=['GET'])
def list():
    urls = utils.get_shot_urls()
    shots = requests.get(url).json()
    return render_template('shots/list.html', shots=shots)


@mod.route('/detail/<int:shot_id>/', methods=['GET'])
def detail(shot_id):
    url = utils.get_url(path='shots/%s' % shot_id)
    shot = requests.get(url).json()
    return render_template('shots/detail.html', shot=shot)
