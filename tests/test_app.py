from flask import Flask, request, Blueprint
from flask_apidoc import APIDoc
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)

a_bp = Blueprint('abp', __name__, url_prefix='/abp')
b_bp = Blueprint('bbp', __name__, url_prefix='/bbp')


@app.route('/')
def index():
    """ hello world
    """
    return '456'

@a_bp.route('/<hello>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index(hello):
    return '123'


@b_bp.route('/')
def index():
    """
    desc: 测试接口
    get:
        desc: 测试接口
        param:
            ok: { 'type': str, 'required': False, 'default': 0, 'desc': '测试用' }
            hello: { 'type': int, 'required': True, 'default': 1}
        resp:
            {
                'ok': 123,
                'haha': 'ok',
            }
    """
    return '789'

class Hello(Resource):
    """
    desc: 测试接口
    get:
        desc: 测试接口
        param:
            ok: { 'type': str, 'required': False, 'default': 0, 'desc': '测试用' }
            hello: { 'type': int, 'required': True, 'default': 1}
        resp:
            {
                'ok': 123,
                'haha': 'ok',
            }
    post:
        desc: 测试接口
    """
    def get(self, id):
        return 'hello, 123'
    
    def post(self):
        pass

app.register_blueprint(a_bp)
app.register_blueprint(b_bp)
api.add_resource(Hello, '/hello/<id>')
APIDoc(app)


if __name__ == '__main__':
    app.run(debug=True)