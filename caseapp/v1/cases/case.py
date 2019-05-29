import datetime


from flask import g,make_response, jsonify
from flask_restful import Resource, reqparse

from caseapp.v1.cases.model import CaseModel
from caseapp.v1.utils.decorators import jwt_token_required
from caseapp.v1.utils.validations import validate_case_data_empty


class CaseView(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('registry',help="provide the registry")
        parser.add_argument('case_type',help="provide a case_type")
        parser.add_argument('file_date',help="provide the return file date ")
        parser.add_argument('brought_forward',help="provide the number of cases brought_forward", type=int)
        parser.add_argument('filed',help="provide the number of cases filed", type=int)
        parser.add_argument('disposed',help="provide the number of cases disposed", type=int)
        parser.add_argument('staff_reg',help="provide a staff user_id", type=int)
        parser.add_argument('designation',help="provide the return designation")
        self.args =parser.parse_args()

    @jwt_token_required
    def post(self):
        case_data=self.args
        check_empty_data= validate_case_data_empty(case_data=case_data)
        if check_empty_data:
            return{
                'status':'401',
                'message':check_empty_data
            }, 401
        clean_data=case_data
        createdon= datetime.datetime.utcnow()
        createdby=g.active_user
        registry=clean_data['registry']
        case_type=clean_data['case_type']
        file_date =clean_data['file_date']
        brought_forward=clean_data['brought_forward']
        filed=clean_data['filed']
        disposed=clean_data['disposed']
        staff_reg=clean_data['staff_reg']
        designation=clean_data['designation']
        check_dublicate_cases=CaseModel().check_double_entry(registry, case_type, file_date )
        if check_dublicate_cases:
            return{
            'status':"Failed",
            'message':"A similar/dublicate case does exist"}
        save_cases= CaseModel().save_cases(createdon, createdby,registry, case_type, file_date ,brought_forward, filed, disposed,staff_reg, designation)
        return{
        'status':'201',
        'message':"case saved"}

    @jwt_token_required
    def get(self):
        get_all= CaseModel().get_all_cases()
        if get_all is None:
            return{
            'status':"Failed",
            'message':"No case found"}
        return make_response(jsonify({
            'status':"success",
            'message':get_all
            }))
       

        
