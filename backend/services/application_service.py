from model import Application, db, Student, PlacementDrive, Company
from services.service_errors import ServiceError
from datetime import date


class ApplicationService:

    @staticmethod
    def get_all():
        return Application.query.all()

    @staticmethod
    def get_by_id(id):
        item = Application.query.get(id)

        if not item:
            raise ServiceError("Application not found")

        return item

    @staticmethod
    def check_eligibility(student_id, drive_id):
        """
        Check if a student is eligible to apply for a drive based on CGPA and branch constraints.
        Returns: dict with 'eligible' (bool) and 'reasons' (list of reasons if not eligible)
        """
        student = Student.query.get(student_id)
        drive = PlacementDrive.query.get(drive_id)
        
        if not student:
            raise ServiceError("Student not found")
        if not drive:
            raise ServiceError("Drive not found")

        reasons = []

        if not student.is_active:
            reasons.append("Student is blacklisted")

        if drive.status != "approved":
            reasons.append("Drive is not open for applications")

        company = Company.query.get(drive.company_id)
        if company and company.status == "blacklisted":
            reasons.append("Company is blacklisted")
        
        # Check CGPA eligibility
        if drive.min_cgpa and (student.cgpa is None or student.cgpa < drive.min_cgpa):
            reasons.append(f"Your CGPA ({student.cgpa or 'Not set'}) is below the minimum required CGPA of {drive.min_cgpa}")
        
        # Check branch eligibility
        if drive.eligibility_branch and drive.eligibility_branch.lower() != "all" and drive.eligibility_branch.lower() != "all branches":
            allowed_branches = [b.strip().lower() for b in drive.eligibility_branch.split(",")]
            if not student.branch or student.branch.strip().lower() not in allowed_branches:
                reasons.append(f"Your branch ({student.branch or 'Not set'}) does not match the required branch ({drive.eligibility_branch})")
        
        return {
            "eligible": len(reasons) == 0,
            "reasons": reasons
        }

    @staticmethod
    def create(data):
        # Check eligibility before creating application
        if "student_id" in data and "drive_id" in data:
            eligibility = ApplicationService.check_eligibility(data["student_id"], data["drive_id"])
            if not eligibility["eligible"]:
                raise ServiceError("Not eligible: " + " | ".join(eligibility["reasons"]))

            existing = Application.query.filter_by(
                student_id=data["student_id"],
                drive_id=data["drive_id"]
            ).first()
            if existing:
                raise ServiceError("Already applied for this drive")
        
        if "applied_date" not in data or not data["applied_date"]:
            data["applied_date"] = date.today()
        item = Application(**data)

        db.session.add(item)
        db.session.commit()

        return item

    @staticmethod
    def update(data):
        item = Application.query.get(data["id"])

        if not item:
            raise ServiceError("Application not found")

        for key, value in data.items():
            if key != "id" and hasattr(item, key):
                setattr(item, key, value)

        db.session.commit()

        return item

    @staticmethod
    def get_by_student(student_id):
        return Application.query.filter_by(student_id=student_id).all()

    @staticmethod
    def get_by_drive(drive_id):
        return Application.query.filter_by(drive_id=drive_id).all()

    @staticmethod
    def delete(id):
        item = Application.query.get(id)

        if not item:
            raise ServiceError("Application not found")

        db.session.delete(item)
        db.session.commit()