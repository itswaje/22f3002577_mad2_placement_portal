from flask_restful import Resource, marshal, fields
from flask import request
from services.student_service import StudentService
from services.service_errors import ServiceError
from flask_security import current_user
from flask_security.decorators import roles_required, auth_required
from extentions import cache

student_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "name": fields.String,
    "branch": fields.String,
    "year": fields.Integer,
    "cgpa": fields.Float,
    "skills": fields.String,
    "is_active": fields.Boolean,
}


class StudentMeResource(Resource):

    @auth_required("token")
    @roles_required("student")
    def get(self):
        from model import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404
        return marshal(student, student_fields), 200


class StudentResource(Resource):

    @auth_required("token")
    def get(self, id):
        try:
            item = StudentService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("student") and item.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        return marshal(item, student_fields), 200

    @auth_required("token")
    def put(self, id):
        try:
            item = StudentService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("student") and item.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        data = request.get_json()
        item = StudentService.update(id, data)
        cache.delete("student_list")
        return marshal(item, student_fields), 200

    @auth_required("token")
    def delete(self, id):
        try:
            item = StudentService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        # only admin can delete students
        if not current_user.has_role("admin"):
            return {"message": "Not authorized"}, 403

        StudentService.delete(id)
        cache.delete("student_list")
        return {"message": "Student deleted successfully"}, 200


class StudentListResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    @cache.cached(key_prefix="student_list")
    def get(self):
        items = StudentService.get_all()
        return marshal(items, student_fields), 200

    @auth_required("token")
    @roles_required("student")
    def post(self):
        data = request.get_json()
        data["user_id"] = current_user.id

        item = StudentService.create(data)
        cache.delete("student_list")
        return marshal(item, student_fields), 201


class StudentExportCSVResource(Resource):
    """POST /api/students/me/export-csv  — triggers async CSV export job."""

    @auth_required("token")
    @roles_required("student")
    def post(self):
        from model import Student
        from tasks.export_tasks import export_applications_csv

        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404

        task = export_applications_csv.delay(student.id)
        return {
            "message": "Export started. You will receive an email with the CSV shortly.",
            "task_id": task.id,
        }, 202
