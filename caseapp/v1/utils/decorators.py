import functools

from flask import g, request


from caseapp.v1.auth.model import UserModel
from caseapp.v1.utils.validations import decode_auth_token


def jwt_token_required(f):
    """[summary]
    *@jwt_token_requied
    modarating resouces access based on the authenticity of the token,
    existance of the user and admin approval of the user account
    
    """

    @functools.wraps(f)
    def decorator_token_auth(*args, **kwargs):
        """[jwt required decorator..custom made]
        
        *start bychecking if the header has an authorisation token
        *if true, then split the token and extract the one on index [1]..[sub]
        *now decode the [sub] to get the payload used to encode it
        *use isisntance to check the decoded results is of int type,
        coz we used the user_id from user table to encode
        *if its true, find the user represented by that user_id from db, 
        it will return either a user or none
        *when a user is returned, not None, check if the admin has approved that account, 
        to access the resouces.
        * if it is true,then we use flask.g module to store the, 
        user data into g.active_user
        * the rest are else handlers incase of error

            
        """
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            if auth_token:
                resp = decode_auth_token(auth_token)
                if isinstance(resp, int):
                    active_user = UserModel().find_existing_id(user_id=resp)
                    if active_user:
                        is_auth_status =UserModel().find_user_is_auth_status(resp)
                        if is_auth_status is True:
                            g.active_user = resp
                            return f(*args, **kwargs)
                        else:
                            return{
                            'status': 401,
                            'message':'Your account has been deactivated waiting review'
                            },401
                    else:
                        return{
                    'status': '401',
                    'message':'user does not exist,'
                              'invalid token'},400
                else:
                    return {
                    'status': '401',
                    'message':resp
                    },400
            else:
                return {
                        'status': '401',
                        'message':"invalid authorisation token!!, login again to get another"
                        },400
        else:
            return{
                    'status': '401',
                    'message':"Your request has no authorisation header!!,log in first"
                },401
        
    return decorator_token_auth

def jwt_admin_required(f):

    @functools.wraps(f)
    def decorator_admin_token_auth(*args, **kwargs):
        is_auth_status =UserModel().find_user_is_admin_status(g.active_user)
        if is_auth_status is not True:
            return{
                            'status': 401,
                            'message':'The resource can only be accessed by the admin'
                            },401
        return f(*args, **kwargs)
     
    return decorator_admin_token_auth

