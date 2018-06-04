from flask import request, Blueprint, Flask
from flask_apidoc import views
from types import MethodType
from functools import wraps, update_wrapper
from collections import OrderedDict
import yaml

_api_list = OrderedDict()


def fire_event_bp(func, apidoc):
    """ 蓝图装饰器, 装饰实例方法"""
    @wraps(func)
    def wrapper(app, *args, **kw):
        ret = func(*args, **kw)
        apidoc.show_functions(app)
        return ret
    return wrapper


class _Api(object):

    def __init__(self, url, endpoint, methods, func):
        self.url = url
        self.endpoint = endpoint
        self.func = func
        if methods:
            self._methods = [method.upper() for method in methods]
        else:
            self._methods = []
        self.parser = _DOCParser(self)
    
    def method_doc(self, method):
        return self.parser.handle(method)
    
    def _doc(self):
        return self.func.__doc__

    @property
    def hash_key(self):
        return hash(self.endpoint)
    
    @property
    def methods(self):
        methods = []
        _methods = ['GET', 'POST', 'PUT', 'DELETE']
        for method in _methods:
            if method in self._methods:
                methods.append(method)
        return methods

    def __hash__(self):
        return self.hash_key

    def __eq__(self, other):
        if not getattr(other, 'hash_key'):
            return False
        return self.hash_key == other.hash_key

    def __repr__(self):
        return '<Api url: {}, endpoint: {}>'.format(self.url, self.endpoint)


class _DOCParser(object):

    def __init__(self, api):
        self.api = api

    def handle(self, method):
        try:
            docs = yaml.load(self.api._doc())
            self.docs = self._key_upper(docs) or {}
        except Exception as e:
            self.docs = {'desc': self.api._doc()}
        return self.info(method)
    
    def _key_upper(self, docs):
        return {k.upper(): v for k, v in docs.items()}
    
    def _method_info(self, method):
        """ 文档信息"""
        method_info = self.docs.get(method, {})
        return method_info
    
    def info(self, method):
        info = self._method_info(method)
        return info

class APIDoc(object):

    def __init__(self, app=None):
        self.load_endpoints = set()
        self.view_functions = {}
        self._hidden_bp_list = ['apidocs']
        self._hidden_endpoints = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('APIDOC_URL', '/apidocs')
        app.config.setdefault('APIDOC_BLUEPRINT_NAME', 'apidocs')

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        self.app = app
        app.extensions['api_doc'] = self
        if app.config['DEBUG']:
            """ 动态的给app register_blueprint加上装饰器"""
            rb = fire_event_bp(self.app.register_blueprint, self)
            self.app.register_blueprint = MethodType(rb, self.app)
            self.configure_blueprint(app)
            self.show_functions(app)

    def configure_blueprint(self, app):
        from flask_apidoc import views
        app.register_blueprint(views.bp)
    
    def hidden_blueprint(self, bp):
        """ 忽略的blueprint"""
        self._hidden_bp_list.add(bp)
    
    def is_hidden_endpoint(self, endpoint):
        """ 过滤endpoint"""
        bp_name = endpoint.split('.')[0]
        if bp_name in self._hidden_bp_list:
            return True
        else:
            return False
    
    def show_functions(self, app):
        """ 显示的函数"""
        view_functions = app.view_functions
        for endpoint, func in view_functions.items():
            if 'static' in endpoint:
                continue
            if endpoint in self.load_endpoints:
                continue

            self.view_functions[endpoint] = func
        self.parse_app_rules()
    
    def is_first_rule(self, rule):
        """ 第一次加载规则"""
        endpoint = rule.endpoint
        result = (
            endpoint in self.view_functions and
            endpoint not in self.load_endpoints and
            not self.is_hidden_endpoint(endpoint)
        )
        return result
    
    def parse_app_rules(self):
        """ 解析所有规则"""
        global _api_list
        rules = self.app.url_map._rules
        for rule in rules:
            endpoint = rule.endpoint
            if self.is_first_rule(rule):
                func = self.view_functions[endpoint]
                self.load_endpoints.add(endpoint)
                api = _Api(rule.rule, endpoint, rule.methods, func)
                _api_list[endpoint] = api
