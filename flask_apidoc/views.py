
from flask import Blueprint, current_app, render_template
from flask_apidoc.utils import templates_path

bp = Blueprint('apidocs', __name__, url_prefix='/apidocs', template_folder=templates_path)


@bp.route('/')
def index():
    return render_template('index.html')