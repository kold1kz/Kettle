"""views.py"""
from app import app

@app.route('/')
@app.route('/index')
def index():
    """index kakoi-to"""
    return "hello, world!"
