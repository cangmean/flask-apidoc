# flask-apidoc
在线接口文档接口

### 使用
```python
from flask import Flask
from flask_apidoc import APIDoc

app = Flask(__name__)
APIDoc(app)


@app.route('/')
def index():
    return 'Hello flask api doc'
```