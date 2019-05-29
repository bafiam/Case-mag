class DatabaseTables():
    """Database class"""

    def table_query(self):
        users = """CREATE TABLE IF NOT EXISTS users(
        user_id serial not null unique,
        username char varying(255) not null unique ,
        email char varying(255) not null,
        is_admin boolean  default False,
        registered timestamp,
        password char varying(500) not null,
        is_auth boolean  default False,
        PRIMARY KEY(user_id)
        
            )"""
        staff = """CREATE TABLE IF NOT EXISTS staff(
        staff_id serial not null unique,
        first_name char varying(255)not null,
        surname char varying(255)not null,
        other_name char varying(255)not null,
        pj_no int not null unique,
        add_by int not null,
        PRIMARY KEY(staff_id),
        FOREIGN KEY(add_by) REFERENCES users( user_id )ON UPDATE CASCADE
        
        
            )"""
        case_entry = """CREATE TABLE IF NOT EXISTS case_entry(
        incident_id serial not null unique ,
        createdon timestamp not null ,
        createdby int not null ,
        registry char varying(255) not null ,
        case_type char varying(255) not null ,
        file_date date NOT NULL,
        brought_forward int not null,
        filed int not null, 
        disposed int not null, 
        staff_reg int,
        designation char varying(255) not null, 
        PRIMARY KEY(incident_id),
        FOREIGN KEY(createdby) REFERENCES users(user_id )ON DELETE CASCADE,
        FOREIGN KEY(staff_reg) REFERENCES staff ( staff_id ) ON UPDATE CASCADE

            )"""
        blacklist_tokens = """CREATE TABLE IF NOT EXISTS blacklist_tokens(
        id serial not null unique,
        token char varying(500) not null unique,
        blacklisted_on timestamp not null unique,
        PRIMARY KEY(id)
            )"""
   
        print("All Table created successfully")
        self.table_query = [users,staff, case_entry, blacklist_tokens ]
        return self.table_query

    def drop_table_query(self):
        """Resource for teardown when am testing"""
        drop_users = """DROP TABLE IF EXISTS users CASCADE"""

        drop_case_entry = """DROP TABLE IF EXISTS case_entry """

        drop_staff = """DROP TABLE IF EXISTS staff """

        drop_blacklist_tokens = """DROP TABLE IF EXISTS blacklist_tokens """

        self.drop_query = [drop_users, drop_case_entry, drop_staff, drop_blacklist_tokens ]

        return self.drop_query