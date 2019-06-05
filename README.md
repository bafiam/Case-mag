# Case-mag
This is a case return management system developed using flaskrestfull.
# System Users
 1. Admin
 2. Normal user
 
# Postman overview
 
<img src="https://github.com/bafiam/Case-mag/blob/develop/postman.png"/> 


## Prerequisites
The development environment uses postgres db, hence install postgres before proceeding.
    - Mac OS - `brew install postgresql`
    - linux - `sudo apt-get install postgresql postgresql-contrib`
    - windows - Download postgres [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows)

Once installed create a database named `case-mag`
(for linux and mac OS users)
1. type `psql` in terminal.
2. On postgres interactive interface, type `CREATE DATABASE case-mag;`
3. Grant privileges to the user by typing `GRANT ALL ON DATABASE case-mag to <your-postgres-username>;`
## Installation and set-up
1. Clone the project 
2. create a virtual environment using virtualenv.
3. Install the dependencies - `pip install -r requirements.txt`.

# Technology used
 1. flask restfull
 2. postgres--basic sql
 3. PyJWT-jwt token
 4. flask-restplus

# To create the database
  flask db_migrate

# To drop database
  flask db_drop

# To add a default admin
   flask seed_admin

### Modify and use the existing.
   .env 

# swagger overview

   http://127.0.0.1:5000/docs
   
# url_pref http://127.0.0.1:5000 then.
    Sign_in-->/auth/register
    
    UserLogin-->/auth/login

    Logout-->/auth/logout

    Verify_user-->/admin/verify/user

    AddStaff-->/admin/staff/add

    Staff_CRUD-->/admin/staff/add/<pj_no>

    CaseView-->/cases/returns

    SpecificCase-->/cases/returns/specific

    Specific_case_range-->/cases/returns/specific/range

    PendingCases-->/cases/returns/specific/pending

# Author
Stephen Gumba