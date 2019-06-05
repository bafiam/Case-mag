from flask import Flask
#from flask_restful import Api
from flask_restplus import Api

import caseapp
from instance.config import app_config

from .v1.Blueprint import version_1


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    
    # configure settings 
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


    # Adding the  blueprints
    api=Api(app=app, doc='/docs', title='Judical Case returns API',description='A simple Judical Case returns API that consist of an Admin, and IT staff who enter monthy case returns')

    #Adding routes
    from caseapp.v1.auth.sign import Sign_in
    api.add_resource(Sign_in, '/auth/register')

    from caseapp.v1.auth.login import UserLogin
    api.add_resource(UserLogin,'/auth/login')

    from caseapp.v1.auth.logout import Logout
    api.add_resource(Logout,'/auth/logout')

    from caseapp.v1.admin.verify import Verify_user
    api.add_resource(Verify_user,'/admin/verify/user')

    from caseapp.v1.admin.staff import AddStaff
    api.add_resource(AddStaff,'/admin/staff/add')

    from caseapp.v1.admin.staff import Staff_CRUD
    api.add_resource(Staff_CRUD,'/admin/staff/add/<pj_no>')

    from caseapp.v1.cases.case import CaseView
    api.add_resource(CaseView,'/cases/returns')

    from caseapp.v1.cases.case_filter import SpecificCase
    api.add_resource(SpecificCase,'/cases/returns/specific')

    from caseapp.v1.cases.case_filter import Specific_case_range
    api.add_resource(Specific_case_range,'/cases/returns/specific/range')

    from caseapp.v1.cases.case_filter import PendingCases
    api.add_resource(PendingCases,'/cases/returns/specific/pending')


     # register blueprints
    app.register_blueprint(version_1)
    

    return app
