

from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from flask_restful.utils.cors import make_response

from caseapp.v1.auth.model import UserModel
from caseapp.v1.utils.validations import (authenticate_user, encode_auth_token,
                                          login_data_empty_validation)


class UserLogin(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('username',help="provide your username")
        parser.add_argument('password', help="provide a password")
        self.args =parser.parse_args()

    def post(self):
        login_data=self.args
        check_empty= login_data_empty_validation(login_data)
        if check_empty:
            return {"status": 400,
                    "message": check_empty
                    }, 400
        check_username = UserModel().find_existing_username(str.lower(login_data['username']))
        if not check_username:
            return {"status": 400,
                    "message": "Username or password is incorrect"
                    }, 400
        auth = authenticate_user(login_data['password'], check_username[5])
        if not auth:
                return {"status":400,
                "message": "Username or password is incorrect"
                }, 400
        # generate the auth token
        if check_username and auth:
            token_auth = encode_auth_token(check_username [0])
            if token_auth:
                return {
                    "status":200,
                    "message": "Login successfully",
                    "Access token":token_auth.decode()
                    }, 200
            return {
                    "status":500,
                    "message": "Login failed",
                    "options": "Something went wrong!, try again"
                                                },500
