from extentions import db 
from datetime import datetime,timezone
from flask_security import UserMixin,RoleMixin
class BaseModel(db.Model): #this contains all the repeating fields , it will not create columns its just for inheriting purpose 
    __abstract__= True #tells sqlalchemy not to create table for this 
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),default = lambda:datetime.now(timezone.utc))#here lambda function is used because flask usually creates a data and stores it and retreive it when nullable but now i want it to calculate time everytime, when lambda is used it calls the funciton everytime w/o lambda the value just gest stored 
    updated_at=db.Column(db.DateTime(timezone=True),default = lambda:datetime.now(timezone.utc),onupdate = lambda:datetime.now(timezone.utc) )

class User(BaseModel,UserMixin):
    email = db.Column(db.String(120), unique=True,nullable = False)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200),nullable = False)

    #flask-security specific
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True) #if Active False, then the user will not be able to login
    roles = db.relationship('Role', backref = 'bearers', secondary='user_roles')
    requests= db.relationship('Request',back_populates='user')

class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class UserRoles(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))



class Request (BaseModel):
    #company requests placement drive and it will be shown to admin 
    data = db.Column (db.JSON()) 
    status = db.Column(db.Enum("pending","approved","rejected","blacklisted"),default="pending")
    #who created the request 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    user = db.relationship("User", back_populates="requests")

class Student(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    name = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    skills = db.Column(db.Text)
    resume_path = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)



class Company(BaseModel):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    hr_contact = db.Column(db.String(100))
    status = db.Column(db.Enum("pending","approved","rejected","blacklisted"),default="pending")   


class PlacementDrive(BaseModel):
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),nullable = False)
    company = db.relationship('Company', backref='drives')
    drive_name = db.Column(db.String(150))
    job_title = db.Column(db.String(150))
    job_description = db.Column(db.Text)
    eligibility_branch = db.Column(db.String(100))
    min_cgpa = db.Column(db.Float)
    salary = db.Column(db.Integer)
    skills_required = db.Column(db.Text)
    application_deadline = db.Column(db.Date)
    status = db.Column(db.Enum("pending","approved","closed","rejected","cancelled"),default="pending")

class Application(BaseModel):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable = False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'),nullable = False)
    status = db.Column(db.Enum("applied","shortlisted","waiting","selected","rejected"),default="applied")
    applied_date = db.Column(db.Date)
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id'),)#enforces rule that student cannot apply to the same placement drive more than once


class Placement(BaseModel):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable = False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'),nullable = False)
    joining_date = db.Column(db.Date)

