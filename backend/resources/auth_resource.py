"/login"
"/register"
import uuid
from flask import Blueprint,jsonify,request
from flask_security import verify_password,hash_password

from model import User,Company,Student,db

from flask import current_app #have datastore




auth_bp = Blueprint("auth",__name__,url_prefix="/api/auth")

@auth_bp.route("/login",methods = ['POST'])
def login ():
    data = request.get_json()

    email = data ["email"]
    password = data["password"]

    if (not email or not password):
        return jsonify({"message":"invalid input"}),400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"user not found"}),404   
    if not user.active:
        return jsonify({"message":"account awaiting admin approval"}),403
    
    #these are the things sent to the front end 
    if not verify_password(password,user.password):
        return jsonify({'message':'wrong password'}),400
    
        
    return jsonify({
            "id":user.id,
            "email":user.email,
            "name":user.name,
            "token":user.get_auth_token(),
            "role": user.roles[0].name if user.roles else None
        }),200

@auth_bp.route("/register",methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email= data['email']
    password = data['password']
    role = data['role']

    # company profile fields
    company_name = data.get("company_name")
    industry = data.get("industry")
    location = data.get("location")
    website = data.get("website")
    hr_contact = data.get("hr_contact")   

    # student profile fields
    branch = data.get("branch")
    year = data.get("year")
    cgpa = data.get("cgpa")
    skills = data.get("skills") 

    active = True #if its for company it should be false so that the admin can approve it 
    if not name or not email or not password or role not in ["company","student"]:
        return jsonify({"message":"invalid inputs"}),400
    
    if role == "company":
        active = False #if the admin approves then only accept

    datastore=current_app.datastore

#if already a user exists then new user with same name should not be created
    if User.query.filter_by(email=email).first():
        return {"message":"User already exists"},400


    user = datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        active=active
    )

    role_obj = datastore.find_role(role)
    datastore.add_role_to_user(user, role_obj)

    # create company profile if role is company
    if role == "company":
        company = Company(
            user_id=user.id,
            company_name=name,
            industry=industry,
            location=location,
            website=website,
            hr_contact=hr_contact)
        db.session.add(company)
   # create student profile if role is student
    if role == "student":
        student = Student(
            user_id=user.id,
            name=name,
            branch=branch,
            year=year,
            cgpa=cgpa,
            skills=skills
        )
        db.session.add(student)

    try:
        db.session.commit()
    except:
        return {"message":"error assigning role"},400
    return jsonify({"id":user.id,
            "email":user.email,
            "name":user.name,
            }),201 
    