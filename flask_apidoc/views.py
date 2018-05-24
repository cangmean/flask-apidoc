
from flask import Blueprint, render_template, current_app
from flask_apidoc.utils import templates_path
import flask_apidoc

bp = Blueprint(
    'apidocs',
    __name__,
    url_prefix='/apidocs',
    template_folder=templates_path,
)


@bp.route('/')
def index():
    api_list = flask_apidoc._api_list
    return render_template('index.html', api_list=api_list)