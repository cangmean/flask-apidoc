from flask import Flask, request, Blueprint
from flask_apidoc import APIDoc


app = Flask(__name__)
app.config['DEBUG'] = True


APIDoc(app)
a_bp = Blueprint('abp', __name__, url_prefix='/abp')
b_bp = Blueprint('bbp', __name__, url_prefix='/bbp')


@app.route('/')
def index():
    """ hello world
    """
    return '456'

@a_bp.route('/')
def index():
    return '123'


@b_bp.route('/')
def index():
    """
    get:
        param:
            ok: { 'type': str, 'required': False, 'default': 0 }
            hello: { 'type': str, 'required': True}
        return:
            {
                'ok': 123,
                'haha': 'ok',
            }
    """
    return '789'

app.register_blueprint(a_bp)
app.register_blueprint(b_bp)


if __name__ == '__main__':
    app.run(debug=True)