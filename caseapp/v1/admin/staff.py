from flask_restful import Resource, reqparse
from caseapp.v1.utils.validations import validate_staff_data_not_empty
from caseapp.v1.admin.model import AdminModel
from flask import g
from caseapp.v1.utils.decorators import jwt_admin_required,jwt_token_required

class AddStaff(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('surname',help="provide the staf surname")
        parser.add_argument('first_name',help="provide the staff firstname")
        parser.add_argument('other_name',help="provide the staff last name")
        parser.add_argument('pj_no',help="provide the staff pj_no", type=int)
        self.args =parser.parse_args()

    @jwt_token_required
    @jwt_admin_required
    def post(self):
        admin_data=self.args
        check_empty=validate_staff_data_not_empty(staff_data=admin_data)
        if check_empty is not None:
            return check_empty
        check_if_staff_exist= AdminModel().find_staff(pj_no=admin_data['pj_no'])
        if check_if_staff_exist is not None:
            return{
                "status":"fail",
                "message":"There is a similar staff in the system with that pj_no"
            }, 200
        data=admin_data
        first_name=data['first_name']
        surname=data['surname']
        other_name=data['other_name']
        pj_no=data['pj_no']
        added_by=g.active_user
        save_data= AdminModel().save_staff_data(first_name, surname, other_name, pj_no, added_by)
        return{
                'status':"201",
                'message':'Staff data saved '
            },201

    @jwt_token_required
    @jwt_admin_required 
    def get(self):
        get_all_staff=AdminModel().get_all_staff()
        if get_all_staff is None:
            return{
                'status':'failed',
                'message':'Their is no staff data in the system'
            },400
        else:
            staff_all=[]
            for staff in get_all_staff:
                staff_all.append({
                "first_name":staff[1],
                "surname":staff[2],
                "other_name":staff[3],
                "pj_no":staff[4]
                })
            return{
            "status":"success",
            "staff info":staff_all
            }
        

class Staff_CRUD(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('surname',help="provide the staf surname")
        parser.add_argument('first_name',help="provide the staff firstname")
        parser.add_argument('other_name',help="provide the staff last name")
        self.args =parser.parse_args()

    @jwt_token_required
    @jwt_admin_required       
    def delete(self, pj_no):
        get_staff=AdminModel().find_staff(pj_no)
        if get_staff is None:
            return{
                'status':'failed',
                'message':'The staff with that pj_no does not exist'
            },400
        delete_staff_data=AdminModel().delete_staff(pj_no)
        return{
                'status':200,
                'message':'Staff deleted from the system'
            }, 200

    @jwt_token_required
    @jwt_admin_required 
    def get(self,pj_no):
        get_staff=AdminModel().find_staff(pj_no)
        if get_staff is None:
            return{
                'status':'failed',
                'message':'The staff with that pj_no does not exist'
            },400
        else:
            view_staff=[]
            view_staff.append({
                "first_name":get_staff[1],
                "surname":get_staff[2],
                "other_name":get_staff[3],
                "pj_no":get_staff[4]
                })
            return{
            "status":"success",
            "staff info":view_staff
            }
    def patch(self, pj_no):
        staff_update=self.args
        get_staff=AdminModel().find_staff(pj_no)
        if get_staff is None:
            return{
                'status':'failed',
                'message':'The staff with that pj_no does not exist'
            },400
        update_data=staff_update
        first_name=update_data['first_name']
        surname=update_data['surname']
        other_name=update_data['other_name']
        pj_no=get_staff[4]    

        update_data=AdminModel().update_staff(first_name,surname,other_name, pj_no)
        return{
                'status':"success",
                'message':'Staff info updated'
            }, 200




        






        
        

