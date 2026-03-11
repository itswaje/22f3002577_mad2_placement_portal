#flask security and flask sqlalchemy are the extensions of flask so inorder to make the importing easier i have created this file 
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security 
from flask_caching import cache

db = SQLAlchemy() #creates a database object that Flask will use to interact with the database
security = Security() #creation of security object 