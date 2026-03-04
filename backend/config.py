class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turning off background monitoring 

class LocalDevelopmentConfig(BaseConfig): #localdevconfig inherits baseconfig and has extra too 
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"  #specifies which db to connect to 
    DEBUG = True