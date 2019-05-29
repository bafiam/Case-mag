import datetime
import re

import jwt
from flask import current_app
from jwt.api_jwt import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from caseapp.v1.auth.model import UserModel

def user_data_empty_validation(userdata):
    if not userdata['username']:
        return {'error': 'Username required'}
    if not userdata['email']:
        return {'error': 'email required'}
    if not userdata['password']:
        return {'error': 'password required'}
    return None

def username_sign_validate(data):
    if not re.match("^[A-Za-z0-9_-]*$",data['username']):
        return {'error': ' Username can only contains letters, numbers, underscores and dashes'}
    return None

def validate_email(user_email):
    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", user_email['email']):
        return {'error': 'Provide a valid email address'}
    return None

def validate_password(user_password):
    if len(user_password['password']) < 7:
        return {'error': 'Password must be at least 8 characters long!'}
    elif re.search('[0-9]', (user_password['password'])) is None:
        return {'error': 'Password must have at least one number in it!'}
    elif re.search('[A-Z]', (user_password['password'])) is None:
        return {'error': 'Password must have at least one capital letter in it!'}
    elif re.search('[a-z]', (user_password['password'])) is None:
        return {'error': 'Password must have at least one alphabet letter in it!'}
    elif re.search('[!,#,$,%,&,*,+,-,<,=,>,?,@,^,_,{,|,},~,]', (user_password['password'])) is None:
        return {'error': 'Password must have at least a special character in it!'}
    return None

def hash_user_password(user_password):
    hash_pass = generate_password_hash(user_password)
    return hash_pass

def authenticate_user(db_password, password):
    check_pass= check_password_hash(password,db_password)
    
    return check_pass
def login_data_empty_validation(logindata):
    if not logindata['username']:
        return {'error': 'Username required'}
    if not logindata['password']:
        return {'error': 'password required'}
    return None

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=80),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        auth_encoded=jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        auth_encoded=jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return auth_encoded
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        is_blacklisted_token =UserModel().check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        is_blacklisted_exp_token =UserModel().check_blacklist(auth_token)
        if not is_blacklisted_exp_token:
            blacklist_token_exp = UserModel().save_blacklist_tokens(auth_token)
            return 'Signature expired. Please log in again.'
        return 'Token blacklisted. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def authenticate_active_token(active_token):
    auth_header = active_token
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = decode_auth_token(auth_token)
        #encode with an int soo if the resp is a string return false
        #factor in if not false == true
        if not isinstance(resp, str):
            blacklist_token = UserModel().save_blacklist_tokens(auth_token)
            return{
                    'status': 'success',
                    'message': 'Successfully logged out.'
                    
                },200
        return{
                    'status': 'failed',
                    'message': resp
                },401
    return{
            'status': 'fail',
            'message': 'Provide a valid auth token.'
                },403

def validate_admin_verify(data):
    if not data['user_username']:
        return {'error': 'A registed user,[Username] is required'}
    return None

def validate_staff_data_not_empty(staff_data):
    if not staff_data['surname']:
        return {'error': 'surname required'}
    if not staff_data['first_name']:
        return {'error': 'first_name required'}
    if not staff_data['other_name']:
        return {'error': 'last_name required'}
    if not staff_data['pj_no']:
        return {'error': 'pj_no required'}
    return None

def validate_case_data_empty(case_data):
    if not case_data['registry']:
        return {'error':'registry required'}
    if not case_data['case_type']:
        return {'error':'case_type required'}
    if not case_data['file_date']:
        return {'error':'A file_date  required'}
    if not case_data['brought_forward']:
        return {'error':'cases brought_forward required'}
    if not case_data['filed']:
        return {'error':'cases filed required'}
    if not case_data['disposed']:
        return {'error':'cases disposed required'}
    if not case_data['staff_reg']:
        return {'error':'A staff_reg is required'}
    if not case_data['designation']:
        return {'error':'A return designation is required'}
    return None
def validate_specific_case_data_empty(case_data):
    if not case_data['registry']:
        return {'error':'registry required'}
    if not case_data['case_type']:
        return {'error':'case_type required'}
    if not case_data['file_date']:
        return {'error':'A file_date  required'}
    return None
def validate_specific_range_data_empty(case_data):
    if not case_data['registry']:
            return {'error':'registry required'}
    if not case_data['case_type']:
        return {'error':'case_type required'}
    if not case_data['from']:
        return {'error':'An year from required'}
    if not case_data['to']:
        return {'error':'A year to required'}
    return None
def validate_pending_cases_data_empty(case_data):
    if not case_data['registry']:
        return {'error':'registry from required'}
    if not case_data['from']:
        return {'error':'An year from required'}
    if not case_data['to']:
        return {'error':'A year to required'}
    return None

