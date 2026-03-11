from flask_restful import Resource, marshal, fields
from services.application_service import ApplicationService
from flask_security import current_user
from flask_security.decorators import roles_required, roles_accepted, auth_required
from flask import request

application_fields = {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "drive_id": fields.Integer,
    "status": fields.String,
    "applied_date": fields.String,
}


# GET /api/applications
# POST /api/applications
class ApplicationListResource(Resource):

    @auth_required("token")
    @roles_accepted("admin", "company")
    def get(self):
        items = ApplicationService.get_all()
        return marshal(items, application_fields), 200

    @auth_required("token")
    @roles_required("student")
    def post(self):
        data = request.get_json()

        from model import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404
        data["student_id"] = student.id

        try:
            item = ApplicationService.create(data)
            return marshal(item, application_fields), 201
        except Exception as e:
            error_msg = str(e)
            # Check if it's an eligibility error
            if "Not eligible:" in error_msg:
                return {
                    "message": error_msg.replace("Not eligible: ", ""),
                    "type": "eligibility_error"
                }, 403
            return {"message": error_msg}, 400


# GET /api/eligibility/<drive_id> - Check eligibility for a drive
class EligibilityResource(Resource):

    @auth_required("token")
    @roles_required("student")
    def get(self, drive_id):
        from model import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404
        
        try:
            eligibility = ApplicationService.check_eligibility(student.id, drive_id)
            return eligibility, 200
        except Exception as e:
            return {"message": str(e)}, 400


# GET /api/applications/<id>
# PATCH /api/applications/<id>
# DELETE /api/applications/<id>
class ApplicationResource(Resource):

    @auth_required("token")
    def get(self, id):
        try:
            item = ApplicationService.get_by_id(id)
            if current_user.has_role("student"):
                from model import Student
                student = Student.query.filter_by(user_id=current_user.id).first()
                if not student or item.student_id != student.id:
                    return {"message": "Not authorized"}, 403
            elif current_user.has_role("company"):
                from model import Company, PlacementDrive
                company = Company.query.filter_by(user_id=current_user.id).first()
                drive = PlacementDrive.query.get(item.drive_id)
                if not company or not drive or drive.company_id != company.id:
                    return {"message": "Not authorized"}, 403
            elif not current_user.has_role("admin"):
                return {"message": "Not authorized"}, 403

            return marshal(item, application_fields), 200
        except Exception as e:
            return {"message": str(e)}, 404

    @auth_required("token")
    @roles_accepted("admin", "company")
    def patch(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            item = ApplicationService.update(data)
            return marshal(item, application_fields), 200
        except Exception as e:
            return {"message": str(e)}, 400

    @auth_required("token")
    def delete(self, id):
        try:
            item = ApplicationService.get_by_id(id)
        except Exception as e:
            return {"message": str(e)}, 404

        if current_user.has_role("student"):
            from model import Student
            student = Student.query.filter_by(user_id=current_user.id).first()
            if not student or item.student_id != student.id:
                return {"message": "Not authorized"}, 403

        if current_user.has_role("company"):
            return {"message": "Not authorized"}, 403

        ApplicationService.delete(id)
        return {"message": "Application deleted"}, 200


# GET /api/drives/<drive_id>/applications
class DriveApplicationsResource(Resource):

    @auth_required("token")
    @roles_accepted("admin", "company")
    def get(self, drive_id):
        items = ApplicationService.get_by_drive(drive_id)
        return marshal(items, application_fields), 200


# GET /api/drives/<drive_id>/applications/details
class DriveApplicationsDetailedResource(Resource):

    @auth_required("token")
    @roles_accepted("admin", "company")
    def get(self, drive_id):
        from model import Student, Company, PlacementDrive

        if current_user.has_role("company"):
            company = Company.query.filter_by(user_id=current_user.id).first()
            drive = PlacementDrive.query.get(drive_id)
            if not company or not drive or drive.company_id != company.id:
                return {"message": "Not authorized"}, 403

        items = ApplicationService.get_by_drive(drive_id)

        student_ids = {item.student_id for item in items}
        students = Student.query.filter(Student.id.in_(student_ids)).all() if student_ids else []
        student_map = {
            s.id: {
                "id": s.id,
                "name": s.name,
                "branch": s.branch,
                "year": s.year,
                "cgpa": s.cgpa,
            }
            for s in students
        }

        data = []
        for item in items:
            data.append({
                "id": item.id,
                "student_id": item.student_id,
                "drive_id": item.drive_id,
                "status": item.status,
                "applied_date": str(item.applied_date) if item.applied_date else None,
                "student": student_map.get(item.student_id),
            })

        return data, 200


# GET /api/students/<student_id>/applications
class StudentApplicationsResource(Resource):

    @auth_required("token")
    def get(self, student_id):
        if current_user.has_role("student"):
            from model import Student
            student = Student.query.filter_by(user_id=current_user.id).first()
            if not student or student.id != student_id:
                return {"message": "Not authorized"}, 403
        items = ApplicationService.get_by_student(student_id)
        return marshal(items, application_fields), 200


# GET /api/students/<student_id>/applications/details
class StudentApplicationsDetailedResource(Resource):

    @auth_required("token")
    def get(self, student_id):
        from model import Student, PlacementDrive, Company

        if current_user.has_role("student"):
            student = Student.query.filter_by(user_id=current_user.id).first()
            if not student or student.id != student_id:
                return {"message": "Not authorized"}, 403
        elif not current_user.has_role("admin"):
            return {"message": "Not authorized"}, 403

        items = ApplicationService.get_by_student(student_id)

        drive_ids = {item.drive_id for item in items}
        drives = PlacementDrive.query.filter(PlacementDrive.id.in_(drive_ids)).all() if drive_ids else []

        company_ids = {d.company_id for d in drives if d.company_id}
        companies = Company.query.filter(Company.id.in_(company_ids)).all() if company_ids else []
        company_map = {c.id: c.company_name for c in companies}

        drive_map = {}
        for d in drives:
            drive_map[d.id] = {
                "id": d.id,
                "company_id": d.company_id,
                "company_name": company_map.get(d.company_id),
                "drive_name": d.drive_name,
                "job_title": d.job_title,
                "salary": d.salary,
                "status": d.status,
            }

        data = []
        for item in items:
            data.append({
                "id": item.id,
                "student_id": item.student_id,
                "drive_id": item.drive_id,
                "status": item.status,
                "applied_date": str(item.applied_date) if item.applied_date else None,
                "drive": drive_map.get(item.drive_id),
            })

        return data, 200
