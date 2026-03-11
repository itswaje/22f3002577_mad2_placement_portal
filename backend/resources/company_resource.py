from flask import request
from flask_restful import Resource, marshal, fields
from services.company_service import CompanyService
from services.drive_service import DriveService
from services.service_errors import ServiceError
from flask_security import current_user
from flask_security.decorators import roles_required, auth_required
from .drive_resource import marshal_fields as drive_fields

company_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "company_name": fields.String,
    "industry": fields.String,
    "location": fields.String,
    "website": fields.String,
    "hr_contact": fields.String,
    "status": fields.String
}


class CompanyResource(Resource):

    # GET /api/companies/<id>
    @auth_required("token")
    def get(self, id):
        try:
            item = CompanyService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("company") and item.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        return marshal(item, company_fields), 200

    # PUT /api/companies/<id>
    @auth_required("token")
    def put(self, id):
        try:
            item = CompanyService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("company") and item.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        data = request.get_json()
        item = CompanyService.update(id, data)

        return marshal(item, company_fields), 200

    # DELETE /api/companies/<id>
    @auth_required("token")
    def delete(self, id):
        try:
            item = CompanyService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("company") and item.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        CompanyService.delete(id)
        return {"message": "Company deleted successfully"}, 200


class CompanyListResource(Resource):

    # GET /api/companies — anyone logged in can view companies
    @auth_required("token")
    def get(self):
        items = CompanyService.get_all()
        return marshal(items, company_fields), 200

    # POST /api/companies — company user registers their profile
    @auth_required("token")
    @roles_required("company")
    def post(self):
        data = request.get_json()
        data["user_id"] = current_user.id

        item = CompanyService.create(data)
        return marshal(item, company_fields), 201


class CompanyDrivesResource(Resource):

    # GET /api/companies/<id>/drives
    @auth_required("token")
    def get(self, id):
        try:
            company = CompanyService.get_by_id(id)
        except ServiceError as e:
            return {"message": str(e)}, 404

        if current_user.has_role("company") and company.user_id != current_user.id:
            return {"message": "Not authorized"}, 403

        drives = DriveService.get_by_company(id)
        return marshal(drives, drive_fields), 200
