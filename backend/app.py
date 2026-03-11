from flask import Flask
from config import LocalDevelopmentConfig
from resources import auth_bp ,api,api_bp# for blueprint (if i didnt create init.py then i would have imported it as resources.auth_resource)
from flask_cors import CORS
import uuid
from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab
from extentions import cache
from celery_factory import celery_init_app
from celery.schedules  import crontab

def ensure_default_data(app, db, datastore, User):
    from flask_security import hash_password
    from model import Student

    datastore.find_or_create_role("admin", description="super user")
    datastore.find_or_create_role("student", description="placement portal student")
    datastore.find_or_create_role("company", description="recruiting company")

    defaults = [
        {
            "email": "admin@gmail.com",
            "name": "admin_01",
            "password": "pass",
            "role": "admin",
            "active": True,
        },
        {
            "email": "company@gmail.com",
            "name": "company_01",
            "password": "passs",
            "role": "company",
            "active": True,
        },
        {
            "email": "student@gmail.com",
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
    from extentions import security ,cache
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app,datastore=datastore,)
    app.datastore = datastore 


    #bluerint 
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # cache
    cache.init_app(app)
    

      # celery config
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0", #this is the redis-server running port
        result_backend="redis://localhost:6379/1",
        timezone = 'Asia/Kolkata',
        include=["tasks.mail_tasks", "tasks.export_tasks"],
    ),
    )
    celery_app = celery_init_app(app)
    #flask restful
    # create database tables
    with app.app_context():
        db.create_all()#creates database and tables
        ensure_default_data(app, db, datastore, User)

    return app,celery_app


app, celery_app = create_app()


from tasks.mail_tasks import send_daily_reminders, send_monthly_report

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # a. Daily reminders –  at 8:0 AM IST (change back to hour=8, minute=0)
    sender.add_periodic_task(
        crontab(hour=8, minute=8),
        send_daily_reminders.s(),
        name="daily-deadline-reminders",
    )

    # b. Monthly activity report – runs on the 1st of every month at 7:00 AM IST
    sender.add_periodic_task(
        crontab(hour=18, minute=12, day_of_month=11),
        send_monthly_report.s(),
        name="monthly-activity-report",
    )


if (__name__=="__main__"):
    app.run(debug=True)

