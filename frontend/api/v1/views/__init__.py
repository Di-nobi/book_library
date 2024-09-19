from flask import Blueprint

app_look = Blueprint('app_look', __name__, url_prefix='/api/v1')

from frontend.api.v1.views.books import *
from frontend.api.v1.views.users import *