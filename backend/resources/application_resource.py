from flask_restful import Resource, marshal, fields
from services.application_service import ApplicationService
from flask_security import current_user
from flask_security.decorators import roles_required, roles_accepted, auth_required
from flask import request

application_fields = {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "drive_id": fields.Integer,
    "status": fields.String
}


# GET /api/applications
# POST /api/applications
class ApplicationListResource(Resource):

    @roles_accepted("admin", "company")
    def get(self):
        items = ApplicationService.get_all()
        return marshal(items, application_fields), 200

    @roles_required("student")
    def post(self):
        data = request.get_json()

        from model import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404
        data["student_id"] = student.id

        item = ApplicationService.create(data)
        return marshal(item, application_fields), 201


# GET /api/applications/<id>
# PATCH /api/applications/<id>
# DELETE /api/applications/<id>
class ApplicationResource(Resource):

    @auth_required()
    def get(self, id):
        try:
            item = ApplicationService.get_by_id(id)
            return marshal(item, application_fields), 200
        except Exception as e:
            return {"message": str(e)}, 404

    @roles_accepted("admin", "company")
    def patch(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            item = ApplicationService.update(data)
            return marshal(item, application_fields), 200
        except Exception as e:
            return {"message": str(e)}, 400

    @auth_required()
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

    @roles_accepted("admin", "company")
    def get(self, drive_id):
        items = ApplicationService.get_by_drive(drive_id)
        return marshal(items, application_fields), 200


# GET /api/students/<student_id>/applications
class StudentApplicationsResource(Resource):

    @auth_required()
    def get(self, student_id):
        if current_user.has_role("student"):
            from model import Student
            student = Student.query.filter_by(user_id=current_user.id).first()
            if not student or student.id != student_id:
                return {"message": "Not authorized"}, 403
        items = ApplicationService.get_by_student(student_id)
        return marshal(items, application_fields), 200
