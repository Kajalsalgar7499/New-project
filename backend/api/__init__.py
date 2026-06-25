from flask import Flask
from flask_cors import CORS

from api.routes import api


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(api, url_prefix="/api")
    return app
