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
    datastore.find_or_create_role("admin", description="super user")
    datastore.find_or_create_role("student", description="placement portal student")
    datastore.find_or_create_role("company", description="recruiting company")

    # create admin user
    if not datastore.find_user(email="admin@study"):
        admin = datastore.create_user(
            email="admin@study",
            name="admin_01",
            password=hash_password("pass"))
        datastore.add_role_to_user(admin, "admin")

    try:
        db.session.commit()
        print("created successfully")
    except Exception as e:
        db.session.rollback()
        print("Error while creating:", e)