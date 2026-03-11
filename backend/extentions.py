#flask security and flask sqlalchemy are the extensions of flask so inorder to make the importing easier i have created this file 
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security 
from flask_caching import Cache

db = SQLAlchemy() #creates a database object that Flask will use to interact with the database
security = Security() #creation of security object 
cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_DEFAULT_TIMEOUT': 300}) #creates a cache object for caching responses