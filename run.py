import datetime
import os

import click
from flask.cli import with_appcontext

from caseapp.app import create_app
from caseapp.v1.auth.model import UserModel
from caseapp.v1.database.config import DatabaseModel
from caseapp.v1.utils.validations import validate_password, hash_user_password

case_mag_app=create_app(os.getenv('FLASK_CONFIG')or 'development')

"""[Using click we can load default values fro command;
it will be getting them from the environment variables
declared in the terminal or in the .env ]
"""
@click.command("db_migrate")
@with_appcontext
def db_migrate():
    DatabaseModel().dbconn(case_mag_app)
    DatabaseModel().create_database_tables()

"""[Innitialize the database connection;
     create the database table]
     [Command]----->>> [flask db_migrate]
     """
case_mag_app.cli.add_command(db_migrate)

@click.command("db_drop")
@with_appcontext
def db_drop ():
     DatabaseModel().dbconn(case_mag_app)
     DatabaseModel().db_drop_table()

case_mag_app.cli.add_command(db_drop)

@click.command("seed_admin")
@with_appcontext
def seed_admin():
     registered = datetime.datetime.now()
     admin_data = {
        "username": case_mag_app.config['SEED_ADMIN_USERNAME'],
        "password": case_mag_app.config['SEED_ADMIN_PASSWORD'],
        "email": case_mag_app.config['SEED_ADMIN_EMAIL'],
        "is_admin": True,
        "registered":registered, 
        "is_auth":True
        }
     check_admin_username= UserModel().find_existing_username(admin_data['username'])
     if check_admin_username is None:
          check_admin_email= UserModel().find_existing_email(admin_data['email'])
          if check_admin_email is None:
               check_admin_password = validate_password(admin_data)
               if check_admin_password is None:
                    verify_data=admin_data
                    username=verify_data['username']
                    password=hash_user_password(verify_data['password'])
                    email=verify_data['email']
                    is_admin=verify_data['is_admin']
                    registered=verify_data['registered']
                    is_auth=verify_data['is_auth']
                    add_admin= UserModel().save_admin_data(username, email, is_admin,registered,password, is_auth)
                    print("admin added")
               else:
                    print(check_admin_password)
          else:
               print("Email already taken")
     else:
          print("Username already taken")
case_mag_app.cli.add_command(seed_admin)
