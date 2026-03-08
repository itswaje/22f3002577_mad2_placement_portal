#python -m scripts.init_db run like this from backend folder
from app import app
from model import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
    db.drop_all() #delete all tables
    db.create_all() #create new tables 

    # get datastore from app
    datastore: SQLAlchemyUserDatastore = app.datastore

    # create roles
    admin_role = datastore.find_or_create_role( "admin",description="super user")
    student_role = datastore.find_or_create_role("student",description="placement portal student")
    company_role = datastore.find_or_create_role("company",description="recruiting company")
    # create users
    #creating admin
    if not datastore.find_user(email="admin@study"):
        admin = datastore.create_user(
        email="admin@study",
        name="admin_01",
        password=hash_password("pass"))
        datastore.add_role_to_user(admin, "admin")


    # create company
    if not datastore.find_user(email="company@study"):
        manager = datastore.create_user(
            email="company@study",
            name="company_01",
            password=hash_password("passs"))
        datastore.add_role_to_user(manager, "company")


    # create student
    if not datastore.find_user(email="student@study"):
        customer = datastore.create_user(
            email="student@study",
            name="student_01",
            password=hash_password("passss"))
    datastore.add_role_to_user(customer, "student")
    try:
        db.session.commit()
        print("created successfully")
    except Exception as e:
        db.session.rollback()
        print("Error while creating:")

#assigning roles to users in the database

    admin_user = datastore.find_user(email="admin@study")
    company_user = datastore.find_user(email="company@study")
    student_user = datastore.find_user(email="student@study")

    admin_role = datastore.find_role("admin")
    company_role = datastore.find_role("company")
    student_role = datastore.find_role("student")

    datastore.add_role_to_user(admin_user, admin_role)
    datastore.add_role_to_user(company_user, company_role)
    datastore.add_role_to_user(student_user, student_role)

    try:
        db.session.commit()
        print("Added roles successfully")
    except:
        db.session.rollback()
        print("Error adding roles")