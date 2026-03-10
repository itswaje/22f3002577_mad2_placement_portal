from flask_restful import Resource
from services.admin_service import AdminService
from services.company_service import CompanyService
from services.service_errors import ServiceError
from flask_security.decorators import roles_required


# /api/admin/dashboard
class AdminDashboardResource(Resource):

    @roles_required("admin")
    def get(self):
        data = AdminService.dashboard()
        return data, 200


# /api/admin/companies/<id>/approve
class CompanyApproveResource(Resource):

    @roles_required("admin")
    def patch(self, id):
        try:
            result = CompanyService.approve_company(id)
            return {"message": result}, 200
        except ServiceError as e:
            return {"message": str(e)}, 400


# /api/admin/companies/<id>/reject
class CompanyRejectResource(Resource):

    @roles_required("admin")
    def patch(self, id):
        result = AdminService.reject_company(id)
        return {"message": result}, 200


# /api/admin/drives/<id>/approve
class DriveApproveResource(Resource):

    @roles_required("admin")
    def patch(self, id):
        result = AdminService.approve_drive(id)
        return {"message": result}, 200


# /api/admin/drives/<id>/reject
class DriveRejectResource(Resource):

    @roles_required("admin")
    def patch(self, id):
        result = AdminService.reject_drive(id)
        return {"message": result}, 200
