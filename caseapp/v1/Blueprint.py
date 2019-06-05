from flask import Blueprint
from flask_restplus import Api


version_1 = Blueprint('CASE-MAG-API', __name__, url_prefix='/api/v1')
api = Api(version_1)