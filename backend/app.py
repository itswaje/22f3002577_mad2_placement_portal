from flask import Flask 
from config import LocalDevelopmentConfig

def create_app():
    
    app=Flask (__name__)
    #config 
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with falsk_sqlalchemy
    from model import db
    db.init_app(app)


    # create database tables(trial)
    with app.app_context():
        db.create_all()#creates database and tables

    return app

app = create_app()

if (__name__=="__main__"):
    app.run(debug=True)

