import requests

from flask import Blueprint, render_template
from app import utils

mod = Blueprint('core', __name__, url_prefix='/')


@mod.route('/', methods=['GET'])
def list():
    shots_by_year = utils.get_shots_by_year()
    return render_template('shots/list.html', shots_by_year=shots_by_year)
