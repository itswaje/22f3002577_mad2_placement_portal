from flask_restful import Resource, marshal, fields
from services.admin_service import AdminService
from services.company_service import CompanyService
from services.student_service import StudentService
from services.request_service import RequestService
from services.service_errors import ServiceError
from flask_security.decorators import roles_required, auth_required

request_fields = {
    "id": fields.Integer,
    "status": fields.String,
    "data": fields.Raw,
    "user_id": fields.Integer,
}


# /api/admin/requests
class AdminRequestsResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def get(self):
        items = RequestService.get_all()
        return marshal(items, request_fields), 200


# /api/admin/dashboard
class AdminDashboardResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def get(self):
        data = AdminService.dashboard()
        return data, 200


# /api/admin/companies/<id>/approve
class CompanyApproveResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        try:
            result = CompanyService.approve_company(id)
            return {"message": result}, 200
        except ServiceError as e:
            return {"message": str(e)}, 400


# /api/admin/companies/<id>/reject
class CompanyRejectResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        result = AdminService.reject_company(id)
        return {"message": result}, 200


# /api/admin/companies/<id>/blacklist
class CompanyBlacklistResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        try:
            result = CompanyService.blacklist_company(id)
            return {"message": result}, 200
        except ServiceError as e:
            return {"message": str(e)}, 400


# /api/admin/students/<id>/blacklist
class StudentBlacklistResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        try:
            result = StudentService.blacklist_student(id)
            return {"message": result}, 200
        except ServiceError as e:
            return {"message": str(e)}, 400


# /api/admin/drives/<id>/approve
class DriveApproveResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        result = AdminService.approve_drive(id)
        return {"message": result}, 200


# /api/admin/drives/<id>/reject
class DriveRejectResource(Resource):

    @auth_required("token")
    @roles_required("admin")
    def patch(self, id):
        result = AdminService.reject_drive(id)
        return {"message": result}, 200
