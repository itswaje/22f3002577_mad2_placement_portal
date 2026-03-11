from flask import Flask
from config import LocalDevelopmentConfig
from resources import auth_bp ,api,api_bp# for blueprint (if i didnt create init.py then i would have imported it as resources.auth_resource)
from flask_cors import CORS
import uuid


def ensure_default_data(app, db, datastore, User):
    from flask_security import hash_password
    from model import Student

    datastore.find_or_create_role("admin", description="super user")
    datastore.find_or_create_role("student", description="placement portal student")
    datastore.find_or_create_role("company", description="recruiting company")

    defaults = [
        {
            "email": "admin@study",
            "name": "admin_01",
            "password": "pass",
            "role": "admin",
            "active": True,
        },
        {
            "email": "company@study",
            "name": "company_01",
            "password": "passs",
            "role": "company",
            "active": True,
        },
        {
            "email": "student@study",
            "name": "student_01",
            "password": "passss",
            "role": "student",
            "active": True,
        },
    ]

    for item in defaults:
        user = datastore.find_user(email=item["email"])
        if not user:
            user = datastore.create_user(
                email=item["email"],
                name=item["name"],
                password=hash_password(item["password"]),
                fs_uniquifier=str(uuid.uuid4()),
                active=item["active"],
            )
        if not any(role.name == item["role"] for role in user.roles):
            datastore.add_role_to_user(user, item["role"])


    db.session.commit()

def create_app():

    app=Flask (__name__)
    #config 
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with falsk_sqlalchemy
    from model import db,User,Role
    db.init_app(app)


    # enable cors 
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"] )
    #flask security things
    from flask_security import SQLAlchemyUserDatastore
    from extentions import security ,Cache
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app,datastore=datastore,)
    app.datastore = datastore 


    #bluerint 
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # cache
    cache.init_app(app)

    #flask restful
    # create database tables(trial)
    with app.app_context():
        db.create_all()#creates database and tables
        ensure_default_data(app, db, datastore, User)

    return app

from datetime import datetime 
app = create_app()

@app.route("/cache")
def cache():
    return datetime.uctnow()


if (__name__=="__main__"):
    app.run(debug=True)

