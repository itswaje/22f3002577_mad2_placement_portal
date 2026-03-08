from flask import Flask 
from config import LocalDevelopmentConfig
from dotenv import load_dotenv #for bringing secret key from the env 

def create_app():
    
    app=Flask (__name__)
    #config 
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with falsk_sqlalchemy
    from model import db,User,Role
    db.init_app(app)

    #flask security things
    from flask_security import SQLAlchemyUserDatastore
    from extentions import security 
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app,datastore=datastore,)#register_blueprint=False
    app.datastore = datastore 




    # create database tables(trial)
    with app.app_context():
        db.create_all()#creates database and tables

    return app

app = create_app()

if (__name__=="__main__"):
    app.run(debug=True)

