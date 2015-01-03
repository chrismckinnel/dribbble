import requests

from flask import Blueprint, render_template
from app import utils

mod = Blueprint('core', __name__, url_prefix='/')


@mod.route('/', methods=['GET'])
def list():
    url = utils.get_url(path='shots')
    shots = requests.get(url).json()
    return render_template('shots/list.html', shots=shots)