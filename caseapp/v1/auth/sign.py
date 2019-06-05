

from flask import jsonify
from flask_restplus import  Resource
from flask_restful import  reqparse
from flask_restful.utils.cors import make_response

from caseapp.v1.auth.model import UserModel
from caseapp.v1.utils.validations import (hash_user_password,
                                          user_data_empty_validation,
                                          username_sign_validate,
                                          validate_email, validate_password)


class Sign_in(Resource):
   
    def __init__(self,*args, **kwargs):
        parser =reqparse.RequestParser()
        parser.add_argument('username',help="provide your username")
        parser.add_argument('email', help="provide your email")
        parser.add_argument('password', help="provide a password")
        parser.add_argument('conf_password', help="Re-enter the password")
        self.args =parser.parse_args()

    def post(self):
        sign_data =self.args
        check_empty= user_data_empty_validation(sign_data)
        if check_empty:
            return {"status": 400,
                    "message": check_empty
                    }, 400
        check_username=username_sign_validate(sign_data)
        if check_username:
            return {"status": 400,
                    "message": check_username
                    }, 400
        check_email=validate_email(sign_data)
        if check_email:
            return {"status": 400,
                    "message": check_email
                    }, 400
        if sign_data['password'] != sign_data['conf_password']:
            return  {"status": 400,
                    "message": 'The passwords dont match'
                    }, 400            
        check_password=validate_password(sign_data)
        if check_password:
            return {"status": 400,
                    "message": check_password
                    }, 400
        check_username_exist = UserModel().find_existing_username(str.lower(sign_data['username']))
        if check_username_exist:
            return {"status": 400,
                    "message": "Username already taken"
                    }, 400
        check_email_exist = UserModel().find_existing_email(sign_data['email'])
        if check_email_exist:
            return {"status": 400,
                    "message": "email already taken"
                    }, 400

        create_account=sign_data
        email = create_account['email']
        username = str.lower(create_account['username'])
        password = hash_user_password(create_account['password'])
        UserModel().save_sign_data(username, email, password)
        return make_response(jsonify({
                    "message": "Registration successfully",
                    "User information": [
                        username
                    ]
                }), 201)

       

