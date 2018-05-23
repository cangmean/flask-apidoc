from flask import request, Blueprint
from flask_apidoc import views


class APIDoc(object):

    def __init__(self, app=None):
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('APIDOC_URL', '/apidocs')
        app.config.setdefault('APIDOC_BLUEPRINT_NAME', 'apidocs')

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['api_doc'] = self
        self.configure_blueprints(app)

    def configure_blueprints(self, app):
        from flask_apidoc import views
        app.register_blueprint(views.bp)