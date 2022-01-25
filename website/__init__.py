from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    
    from .views import views
    
    app.register_blueprint(views, url_prefix="/") 
    return app