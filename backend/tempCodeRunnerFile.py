from flask import Flask 
from config import LocalDevelopmentConfig
from resources import auth_bp ,api,api_bp# for blueprint (if i didnt create init.py then i would have imported it as resources.auth_resource) 

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
    security.init_app(app,datastore=datastore,)
    app.datastore = datastore 


    #bluerint 
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    #flask restful
    #api.init_app(app)



    # create database tables(trial)
    with app.app_context():
        db.create_all()#creates database and tables

    return app

app = create_app()

if (__name__=="__main__"):
    app.run(debug=True)

