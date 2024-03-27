from flask import Blueprint

adminbp  =   Blueprint('admin', __name__)

from . import *