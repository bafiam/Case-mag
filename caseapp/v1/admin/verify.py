from flask_restful import Resource, inputs, reqparse
from flask import g

from caseapp.v1.admin.model import AdminModel
from caseapp.v1.auth.model import UserModel
from caseapp.v1.utils.decorators import (jwt_admin_required,
                                         jwt_token_required)
from caseapp.v1.utils.validations import validate_admin_verify


class Verify_user(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('user_username',help="provide the user, username")
        parser.add_argument('is_auth', help="provide an authorisation state(True or false)", type=inputs.boolean)
        self.args =parser.parse_args()

    @jwt_token_required
    @jwt_admin_required
    def post(self):
        admin_data = self.args
        check_empty_data_fields = validate_admin_verify(data=admin_data)
        if check_empty_data_fields:
            return check_empty_data_fields
        check_user_exist= UserModel().find_existing_username(username=admin_data['user_username'])
        if check_user_exist is None:
            return{
                'status':'failed',
                'message':'The user with that username does not exist'
            },401
        if check_user_exist [0] is g.active_user :
            return{
                'status':'failed',
                'message':'Hey admin, the action will lock you out of the system as an authentic admin '
            },401
            
        update_user_is_auth= AdminModel().update_user_is_auth_status(is_auth=admin_data['is_auth'],username=admin_data['user_username'])
        return{
                'status':400,
                'message':'The user account has been reviewed '
            },400
    
        
