import os
from dotenv import load_dotenv #for bringing secret key from the env

load_dotenv ()     #load environment variable from .env

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turning off background monitoring 
class LocalDevelopmentConfig(BaseConfig): #localdevconfig inherits baseconfig and has extra too
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "instance",
        "database.sqlite3"
    )  #specifies which db to connect to    DEBUG = True
    SECRET_KEY= os.environ.get("SECRET_KEY") #secret value used by Flask to protect sessions and tokens
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") #random string added when generating password hashes
    SECURITY_PASSWORD_HASH = 'argon2'
    WTF_CSRF_ENABLED = False  # disable CSRF for REST API token auth
