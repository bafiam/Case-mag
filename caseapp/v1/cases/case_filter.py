from flask_restful import Resource, reqparse
from flask import make_response, jsonify

from caseapp.v1.utils.decorators import jwt_token_required
from caseapp.v1.utils.validations import validate_specific_case_data_empty, validate_specific_range_data_empty, validate_pending_cases_data_empty
from caseapp.v1.cases.model import CaseModel

class SpecificCase(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('registry',help="provide the registry")
        parser.add_argument('case_type',help="provide a case_type")
        parser.add_argument('file_date',help="provide the return file_date year and month")
        
        self.args =parser.parse_args()

    @jwt_token_required
    def post(self):
        data = self.args
        check_empty=validate_specific_case_data_empty(case_data=data)
        if check_empty:
            return{
                'status':'401',
                'message':check_empty
            }, 401
        clean_data=data
        registry=clean_data['registry']
        case_type=clean_data['case_type']
        file_date =clean_data['file_date']
        
        specific_case=CaseModel().specific_case(registry, case_type,file_date )
        if specific_case is None:
            return{
            'status':"Failed",
            'message':"The case does exist"
            }
        else:
            
            return make_response(jsonify({
        'status':'201',
        'message':specific_case
        }), 201)
class Specific_case_range(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('registry',help="provide the registry")
        parser.add_argument('case_type',help="provide a case_type")
        parser.add_argument('from',help="provide from range year")
        parser.add_argument('to',help="provide  range to year")
        self.args =parser.parse_args()
    @jwt_token_required
    def post(self):
        case= self.args
        check_empty=validate_specific_range_data_empty(case)
        if check_empty:
                return{
                'status':'401',
                'meassage':check_empty
            }, 401
        data=case
        registry=data['registry']
        case_type=data['case_type']
        year_from=data['from']
        year_to=data['to']
        case_range= CaseModel().get_case_by_range(registry, case_type, year_from, year_to)
        if case_range is None:
            return{
            'status':"Failed",
            'message':"No case in that range found "
            }
        
        return make_response(jsonify({
        'status':'sucess',
        'message':case_range
        }))
class PendingCases(Resource):
    def __init__(self):
        parser =reqparse.RequestParser()
        parser.add_argument('registry',help="provide the registry")
        parser.add_argument('from',help="provide from range year")
        parser.add_argument('to',help="provide  range to year")
        self.args =parser.parse_args()
        
    @jwt_token_required
    def post(self):
        pending_data=self.args
        check_empty=validate_pending_cases_data_empty(case_data=pending_data)
        if check_empty:
                return{
                'status':'401',
                'meassage':check_empty
            }, 401
        data=pending_data
        registry=data['registry']
        from_year=data['from']
        to_year=data['to']
        pending=CaseModel().get_pending_cases(registry,from_year, to_year)
        if pending is None:
            return{
            'status':"Failed",
            'message':"No case in that range found "
            }
        
        return make_response(jsonify({
        'status':'sucess',
        'message':pending
        }))


        

        
        
