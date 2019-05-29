import psycopg2
from flask import current_app

from caseapp.v1.database.tables import DatabaseTables

class DatabaseModel:
    """[   
        instanciating the class, calling the config global variables 
        here so as to establish a database connection
        current_app..import from local

        ]
    """
    def __init__(self):
        self.db_host=current_app.config['DB_HOST']
        self.db_user=current_app.config['DB_USER']
        self.db_password=current_app.config['DB_PASSWORD']
        self.db_name=current_app.config['DB_NAME']

        """[instanciate the database connection
        assign local variables]
        """
        self.db_connect=psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
        )
        """instanciate the cursor from the database connection
        """
        self.cursor=self.db_connect.cursor()
        """NB: all cursors do communicate with each other.
         operation done by one cursor with be communicated to all other cursors in the 
         :program
        """
        

    
    def dbconn(self,app):
        """
    establish the database connection based on the traditinal database url
    """
        self.db_connect=psycopg2.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],)
        self.cursor=self.db_connect.cursor()
    

    def create_database_tables(self):
        """call the tables from the tables in the class;
        store them in -->>[tables]--variable;
        execute the query;
        save the operation to the db;
        ensuring consistency

        """
        tables=DatabaseTables().table_query()
        for sql in tables:
            self.db_query(sql)
        self.db_save()


    def db_query(self,query):
        """[execute the given query parameter]
        
        Arguments:
            query {[parameter]} -- [return True]
        """
        self.cursor.execute(query)

    def db_save(self):
        """[ensure the database changes after execution persist]
        """
        self.db_connect.commit()

    def db_close_session(self):
        """[close the database connection, always
        start with the cursor then close the dbconection]
        """
        self.cursor.close()
        self.db_connect.close()

    def db_fetch_all(self):
        """[query the entire db and get all the data;
        entire database rows]
        Returns:
            [rows] --> [the entire database table rows]
        """
        return self.cursor.fetchall()

    def db_fetch_one(self):
        """[query the entire db and get the requested data;
        only the requested row]
        
        Returns:
            [row] -- [only one row from the database]
        """
        return self.cursor.fetchone()

    def db_drop_table(self):

        """[it takes that return list from drop table query;
        loop though a table dropping them one by one;
        then save,[consistency]]
        """
        table_drop = DatabaseTables().drop_table_query()
        for table in table_drop:
            self.drop(table)
        self.db_save()



    def drop(self, name):
        """[drop an existing database.
        The database query will execute a cursor execute based on the name of the table.
        Then commit the execution]
        
        Arguments:
            name {[string]} --> [This will be the database name]
        """
        self.db_query(name)
