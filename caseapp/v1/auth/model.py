import datetime

from caseapp.v1.database.config import DatabaseModel



class UserModel(DatabaseModel):
    def __init__(self):
        super().__init__()
        self.blacklisted_on = datetime.datetime.now()
        self.is_admin= False
        self.registered = datetime.datetime.now()
        

    def find_existing_username(self, username):
        query= """SELECT * FROM users WHERE username = '{0}';""".format(username)
        data=self.db_query(query)
        get_specific_user=self.db_fetch_one()
        self.db_save()
        if get_specific_user:
            return get_specific_user
        return None

    def find_existing_email(self, email):
        query= """SELECT * FROM users WHERE email = '{0}';""".format(email)
        data=self.db_query(query)
        get_specific_email=self.db_fetch_one()
        self.db_save()
        if get_specific_email:
            return get_specific_email
        return None

    def find_existing_id(self, user_id):
        query= """SELECT * FROM users WHERE user_id = '{0}';""".format(user_id)
        data=self.db_query(query)
        get_specific_id=self.db_fetch_one()
        self.db_save()
        if get_specific_id:
            return get_specific_id
        return None

    def save_sign_data(self, username, email, password):
        query = """INSERT INTO users (username, email, password, registered, is_admin) VALUES ('{0}','{1}','{2}', '{3}', '{4}')""".format(username, email, password, self.registered, self.is_admin)
        data= self.db_query(query)
        self.db_save()

    def save_blacklist_tokens(self, token):
        query = """INSERT INTO blacklist_tokens(token, blacklisted_on) VALUES ('{0}','{1}')""".format(token, self.blacklisted_on)
        data= self.db_query(query)
        self.db_save()
        if data:
            return True
        return False
    def check_blacklist(self, auth_token):
        query= """SELECT * FROM blacklist_tokens WHERE token = '{0}';""".format(auth_token)
        data=self.db_query(query)
        resp=self.db_fetch_one()
        self.db_save()
        if resp:
            return True
        return False
    def save_admin_data(self,username, email, is_admin,registered,password, is_auth):
        query = """INSERT INTO users (username, email, is_admin,registered,password, is_auth) VALUES ('{0}','{1}','{2}', '{3}', '{4}', '{5}')""".format(username, email, is_admin,registered,password, is_auth)
        data= self.db_query(query)
        self.db_save()

    def find_user_is_auth_status(self, user_id):
        query= """SELECT * FROM users WHERE user_id = '{0}';""".format(user_id)
        data=self.db_query(query)
        is_auth_status=self.db_fetch_one() [6]
        self.db_save()
        if is_auth_status is True:
            return True
        return False

    def find_user_is_admin_status(self, user_id):
        query= """SELECT * FROM users WHERE user_id = '{0}';""".format(user_id)
        data=self.db_query(query)
        is_admin_status=self.db_fetch_one() [3]
        self.db_save()
        if is_admin_status is True:
            return True
        return False    

