# python -m scripts.seed  running it as a module

import uuid
import random
from faker import Faker
from flask_security.utils import hash_password

from app import app
from model import db, User, Role, Student, Company, PlacementDrive, Application

fake = Faker("en_IN")


def seed_data():

    branches = ["CSE", "IT", "ECE", "EEE"]

    companies = [
        "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra",
        "Zoho", "Freshworks", "Cognizant", "Accenture", "Capgemini"
    ]

    cities = [
        "Bangalore", "Hyderabad", "Chennai",
        "Pune", "Mumbai", "Noida", "Gurgaon"
    ]

    skills_pool = [
        "Python", "Java", "SQL", "Data Structures",
        "Machine Learning", "React", "NodeJS",
        "Docker", "AWS"
    ]

    job_titles = [
        "Software Engineer",
        "Backend Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Full Stack Developer"
    ]

    students = []
    companies_list = []
    drives = []
    applications = []

    # -------------------------
    # Create Roles
    # -------------------------
    student_role = Role.query.filter_by(name="student").first()
    if not student_role:
        student_role = Role(name="student", description="Student role")
        db.session.add(student_role)

    company_role = Role.query.filter_by(name="company").first()
    if not company_role:
        company_role = Role(name="company", description="Company role")
        db.session.add(company_role)

    db.session.commit()

    # -------------------------
    # Create Students
    # -------------------------
    for _ in range(50):

        name = fake.name()
        email = name.lower().replace(" ", ".") + "@student.edu"

        user = User(
            email=email,
            name=name,
            password=hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )

        user.roles.append(student_role)

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            name=name,
            branch=random.choice(branches),
            year=random.randint(2, 4),
            cgpa=round(random.uniform(6.0, 9.8), 2),
            skills=", ".join(random.sample(skills_pool, 5)),
            resume_path="resume.pdf"
        )

        students.append(student)

    db.session.add_all(students)

    # -------------------------
    # Create Companies
    # -------------------------
    for company_name in companies:
        hr_name = fake.name()   # HR person name

        email = f"{company_name.lower().replace(' ', '')}@gmail.com"

        user = User(
            email=email,
            name=hr_name,   # store HR person's name
            password=hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )

        user.roles.append(company_role)

        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id=user.id,
            company_name=company_name,
            industry=random.choice(["IT", "Finance", "AI", "Consulting"]),
            location=random.choice(cities),
            website=f"https://www.{company_name.lower().replace(' ', '')}.com",
            hr_contact="+91" + str(random.randint(9000000000, 9999999999)),
            status="approved"
        )

        companies_list.append(company)

    db.session.add_all(companies_list)
    db.session.commit()

    # -------------------------
    # Placement Drives
    # -------------------------
    companies_db = Company.query.all()

    for _ in range(20):

        company = random.choice(companies_db)

        drive = PlacementDrive(
            company_id=company.id,
            drive_name=f"{company.company_name} Hiring Drive",
            job_title=random.choice(job_titles),
            job_description=fake.text(),
            eligibility_branch=random.choice(["CSE", "IT"]),
            min_cgpa=6.5,
            salary=random.randint(400000, 1200000),
            skills_required=", ".join(random.sample(skills_pool, 4)),
            application_deadline=fake.date_between(start_date="+10d", end_date="+60d"),
            status="approved"
        )

        drives.append(drive)

    db.session.add_all(drives)
    db.session.commit()

    # -------------------------
    # Applications (30)
    # -------------------------
    students_db = Student.query.all()
    drives_db = PlacementDrive.query.all()

    used_pairs = set()

    while len(applications) < 30:

        student = random.choice(students_db)
        drive = random.choice(drives_db)

        if (student.id, drive.id) in used_pairs:
            continue

        used_pairs.add((student.id, drive.id))

        application = Application(
            student_id=student.id,
            drive_id=drive.id,
            status=random.choice([
                "applied",
                "shortlisted",
                "waiting",
                "selected",
                "rejected"
            ]),
            applied_date=fake.date_between(start_date="-10d", end_date="today")
        )

        applications.append(application)

    db.session.add_all(applications)
    db.session.commit()

    print("Fake dataset seeded successfully")


if __name__ == "__main__":
    with app.app_context():
        seed_data()