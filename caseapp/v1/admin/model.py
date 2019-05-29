from builtins import format

from caseapp.v1.database.config import DatabaseModel


class AdminModel(DatabaseModel):
    def __init__(self):
        super().__init__()

    def update_user_is_auth_status(self, is_auth, username):
        query="""UPDATE users SET is_auth = '{0}' WHERE username = '{1}';""".format(is_auth, username)
        data= self.db_query(query)
        self.db_save()

    def find_staff(self, pj_no):
        query="""SELECT * FROM staff WHERE pj_no = '{0}';""".format(pj_no)
        data= self.db_query(query)
        get_specific_staff=self.db_fetch_one()
        self.db_save()
        if get_specific_staff:
            return get_specific_staff
        return None
    def save_staff_data(self, first_name, surname, other_name, pj_no, added_by):
        query="""INSERT INTO staff(first_name, surname, other_name, pj_no, add_by) VALUES ('{0}','{1}', '{2}', '{3}', '{4}')""".format(first_name, surname, other_name, pj_no, added_by)
        data= self.db_query(query)
        self.db_save()

    def delete_staff(self, pj_no):
        query="""DELETE FROM staff WHERE pj_no ='{0}';""".format(pj_no)
        data= self.db_query(query)
        self.db_save()
    
    def get_all_staff(self):
        query="""SELECT * FROM staff;"""
        data= self.db_query(query)
        get_all_staff=self.db_fetch_all()
        self.db_save()
        if get_all_staff:
            return get_all_staff
        return None

    def update_staff(self,first_name, surname, other_name, pj_no):
        query="""UPDATE staff SET first_name='{0}',surname='{1}',other_name='{2}'WHERE pj_no ='{3}';""".format(first_name, surname, other_name, pj_no)
        data= self.db_query(query)
        self.db_save()


