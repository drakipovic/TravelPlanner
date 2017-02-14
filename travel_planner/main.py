import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, ProdConfig, TestConfig

app = Flask('TravelPlanner', static_folder='static', template_folder='templates')
app.root_path = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('PROD', None):
    app.config.from_object(ProdConfig)
else:
    app.config.from_object(TestConfig if os.environ.get('TEST', None) else DevelopmentConfig)


api = Api(app, prefix="/api")
db = SQLAlchemy(app)