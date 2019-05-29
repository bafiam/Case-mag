# Case-mag
This is a case return management system developed using flaskrestfull.
# System Users
 1. Admin
 2. Normal user
 3. Staff
# Postman overview
 
<img src="https://github.com/bafiam/Case-mag/blob/develop/postman.png"/> 



# Technology used
 flask restfull
 postgres--basic sql
 PyJWT-jwt token

# To create the database
  flask db_migrate

# To drop database
  flask db_drop

# To add a default admin
   flask seed_admin

### Modify and use the existing.
   .env 

# url_prefix='/api/v1' then .
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