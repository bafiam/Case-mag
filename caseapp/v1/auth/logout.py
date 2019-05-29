


from flask import request
from flask_restful import Resource

from caseapp.v1.auth.model import UserModel
from caseapp.v1.utils.validations import decode_auth_token, authenticate_active_token


class Logout(Resource):
    def post(self):
        auth_header = request.headers.get('Authorization')
        responce = authenticate_active_token(active_token=auth_header)
        return responce