# flask-apidoc
flask-apidoc 是在线解析接口文档的库。

### 下载
通过github下载到本地后， 进入目录执行以下命令完成安装
```bash
python setup.py install
```

### 用例
flask-apidoc 会读取文档中的yaml格式的内容， 并解析生成api文档。访问接口文档: `http://127.0.0.1:5000/apidocs`
```python
from flask import Flask
from flask_apidoc import APIDoc

app = Flask(__name__)
APIDoc(app)


@app.route('/')
def index():
    """
    get:
        desc: 接口一
        param:
            name: { 'type': str, 'required': True, 'default': 'hello', 'desc': '姓名' }
            age: { 'type': int, 'required': True, 'default': 20}
        resp:
            { 'name': 'hello', 'age': 20}
    """
    return jsonify({'name': 'hello', 'age': 20})
```

### 文档格式
flask-apidoc 解析具有格式的文档
- 一级类别
    - desc 接口的描述
    - method 具体的方法名 get, post, put, delete (目前只支持这些)
- 二级类别
    - desc 具体到方法的接口描述
    - param 参数
        - 参数名 比如: name, age
            - type: 参数类型， 默认string类型
            - required: 参数是否必选, 默认否
            - default: 参数默认值, 默认空字符串
            - desc: 参数描述, 默认空字符串
    - resp 返回值

### 蓝图与MethodView方式
不管是蓝图还是类方式， 解析过程与视图函数是相同的， `DEBUG=False` 时不解析文档。
```python
from flask import Flask, Blueprint, jsonfiy
from flask_apidoc import APIDoc
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)

a_bp = Blueprint('abp', __name__, url_prefix='/abp')

@a_bp.route('/<hello>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index(hello):
    return 'hello'


class Hello(Resource):
    """
    get:
        desc: 接口一
        param:
            name: { 'type': str, 'required': True, 'default': 'hello', 'desc': '姓名' }
            age: { 'type': int, 'required': True, 'default': 20}
        resp:
            { 'name': 'hello', 'age': 20}
    post:
        desc: 测试接口
    """
    def get(self, id):
        return jsonify({'name': 'hello', 'age': 20})
    
    def post(self):
        pass


api.add_resource(Hello, '/hello/<id>')
APIDoc(app)
# 需要注意的是APIDoc 必须在添加视图之后才可以, 使用蓝图不受影响
```
