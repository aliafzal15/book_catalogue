from flask import Blueprint

home = Blueprint('api_home', __name__, url_prefix=('/api'), template_folder='templates')

from bookcat.api_home.views import *
