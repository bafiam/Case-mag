from caseapp.v1.database.config import DatabaseModel

class CaseModel(DatabaseModel):
    def __int__(self):
        super().__init__()

    def map_case(self, data):
            case_data={
                "registry":data[0],
                "case_type":data[1],
                "file_date ":data[2],
                "brought_forward":data[3],
                "filed":data[4],
                "disposed":data[5],
                "staff_reg":data[6],
                "designation":data[7]
            }
            return case_data              
        
    def save_cases(self, createdon, createdby,
         registry, case_type, file_date ,brought_forward, filed, disposed,
         staff_reg, designation):
         query="""INSERT INTO case_entry (createdon,createdby,
         registry,case_type,file_date ,brought_forward,filed,disposed,
         staff_reg,designation) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',
         '{8}','{9}')""".format(createdon, createdby,
         registry, case_type, file_date, brought_forward, filed, disposed,
         staff_reg, designation)
         data= self.db_query(query)
         self.db_save()
    def check_double_entry(self,registry, case_type, file_date ):
        query=""" SELECT 
        registry, case_type, file_date 
        FROM case_entry 
        WHERE 
         registry='{0}' AND case_type='{1}' AND file_date ='{2}' """.format(registry, case_type, file_date )
        data= self.db_query(query)
        get_specific_case=self.db_fetch_one()
        self.db_save()
        if get_specific_case:
            return get_specific_case
        return None

    def specific_case(self,registry, case_type,file_date ):
        query="""SELECT registry, case_type, file_date ,brought_forward, filed, disposed,staff_reg, designation
        FROM case_entry
        WHERE
        registry='{0}' AND case_type='{1}' AND file_date ='{2}'
        """.format(registry, case_type, file_date )
        data=self.db_query(query)
        case=self.db_fetch_one()
        self.db_save()
        if case:
            return self.map_case(case)
        return None
    def get_all_cases(self):
        query= """SELECT registry, case_type, file_date ,brought_forward, filed, disposed,staff_reg, designation FROM case_entry"""
        data=self.db_query(query)
        get_all=self.db_fetch_all()
        self.db_save()
        if get_all:
            cases=[]
            for case in get_all:
                cases.append(self.map_case(case))
            return cases
        return None
    def get_case_by_range(self,registry, case_type, year_from, year_to):
        query="""SELECT registry, case_type, file_date ,brought_forward,filed, disposed,staff_reg, designation 
        FROM case_entry WHERE registry='{0}' AND case_type='{1}' AND file_date 
        BETWEEN '{2}' AND '{3}' ORDER BY file_date;""".format(registry,case_type,year_from,year_to)
        data=self.db_query(query)
        get_range=self.db_fetch_all()
        self.db_save()
        if get_range:
            cases=[]
            for case in get_range:
                cases.append(self.map_case(case))
            return cases
        return None
    def get_pending_cases(self,registry,from_year,to_year):
        query="""SELECT registry, case_type,file_date,brought_forward,filed, disposed,staff_reg, designation 
        FROM case_entry WHERE registry='{0}' AND file_date BETWEEN '{1}' AND '{2}' 
        ORDER BY file_date
        """.format(registry,from_year,to_year)
        data=self.db_query(query)
        get_pending=self.db_fetch_all()
        self.db_save()
        if get_pending:
            cases=[]
            for case in get_pending:
                cases.append(self.map_case(case))
            return cases
        return None




