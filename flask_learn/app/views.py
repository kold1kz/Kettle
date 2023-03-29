"""views.py"""
from app import app
from app import database as dab
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_authorize import Authorize


@app.route('/')
@app.route('/index')
def index():
    """index kakoi-to"""
    return "hello, world!"

@app.route('/admin')
def admin():
    """authorize"""
    
# @app.route('/db')
# def db():
#     """trying to output info about database"""
#     k=dab.Database()
#     return k.dbdisconnect()
