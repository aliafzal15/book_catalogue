from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask('__name__')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'    #flask
bcrypt = Bcrypt(app)

@app.route('/api/')
def api():
    return 'api'


@app.before_request  #This a decorator this is executed before every request, here we can check sessions
def get_something(): #after_request and etc are other decorators
    g.string = '<br> This code ran before my request<br>'

from bookcat.auth import  authentication
from bookcat.api_home import home
app.register_blueprint(home)
app.register_blueprint(authentication)
