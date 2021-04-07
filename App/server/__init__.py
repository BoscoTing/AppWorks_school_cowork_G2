from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from config import Config
import os
import pymysql
from flask_jwt_extended import JWTManager
from waitress import serve
from werkzeug.exceptions import HTTPException
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table

class BaseModel(Model):
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, model_class = BaseModel)
migrate = Migrate(app, db)

jwt = JWTManager()
jwt.init_app(app)

@app.errorhandler(404)
def server_error(error):
    return "Page not found", 404

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return "Internal Server Error", 500

from server.controllers import product_controller, user_controller
