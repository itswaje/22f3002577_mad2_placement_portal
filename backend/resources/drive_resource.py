#http handling
from flask import request
from flask_restful import Resource,marshal,fields,reqparse
from services import DriveService,RequestService
from flask_security import current_user
from flask_security.decorators import roles_required, roles_accepted, auth_required


def _get_company_for_user():
    from model import Company
    return Company.query.filter_by(user_id=current_user.id).first()

# fields returned in API response
marshal_fields = {
    "id": fields.Integer,
    "company_id": fields.Integer,
    "drive_name": fields.String,
    "job_title": fields.String,
    "job_description": fields.String,
    "eligibility_branch": fields.String,
    "min_cgpa": fields.Float,
    "salary": fields.Integer,
    "skills_required": fields.String,
    "application_deadline": fields.String,
    "status": fields.String
}

# request parser for drive creation / update
parser = reqparse.RequestParser()
parser.add_argument("drive_name", type=str, required=True, help="Drive name is required")
parser.add_argument("job_title", type=str, required=True, help="Job title is required")
parser.add_argument("job_description", type=str, required=True, help="Job description is required")
parser.add_argument("eligibility_branch", type=str, required=True, help="Eligibility branch is required")
parser.add_argument("min_cgpa", type=float, required=True, help="Minimum CGPA is required")
parser.add_argument("salary", type=int, required=True, help="Salary is required")
parser.add_argument("skills_required", type=str, required=False)
parser.add_argument("application_deadline", type=str, required=True, help="Application deadline is required")
parser.add_argument("status", type=str, required=False)




#it handles /api/drive/:id
class DriveResource(Resource):

    # anyone logged in can view drives
    @auth_required("token")
    def get(self, id):

        item = DriveService.get_by_id(id)

        if not item:
            return {"message": "Drive not found"}, 404

        return marshal(item, marshal_fields), 200


    @roles_accepted("company", "admin")
    def put(self, id):

        item = DriveService.get_by_id(id)

        if not item:
            return {"message": "Drive not found"}, 404

        args = parser.parse_args()
        args["id"] = id

        if current_user.has_role("company"):
            company = _get_company_for_user()
            if not company or item.company_id != company.id:
                return {"message": "Not authorized"}, 403

            RequestService.create({
                "data": args,
                "status": "pending",
                "user_id": current_user.id
            })
            return {"message": "Update request sent to admin"}, 200

        item = DriveService.update(args)
        return marshal(item, marshal_fields), 200


    @roles_accepted("company", "admin")
    def patch(self, id):

        item = DriveService.get_by_id(id)

        if not item:
            return {"message": "Drive not found"}, 404

        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        data["id"] = id

        if current_user.has_role("company"):
            company = _get_company_for_user()
            if not company or item.company_id != company.id:
                return {"message": "Not authorized"}, 403

            RequestService.create({
                "data": data,
                "status": "pending",
                "user_id": current_user.id
            })
            return {"message": "Update request sent to admin"}, 200

        item = DriveService.update(data)
        return marshal(item, marshal_fields), 200


    @roles_accepted("company", "admin")
    def delete(self, id):

        item = DriveService.get_by_id(id)

        if not item:
            return {"message": "Drive not found"}, 404

        if current_user.has_role("company"):
            company = _get_company_for_user()
            if not company or item.company_id != company.id:
                return {"message": "Not authorized"}, 403

            RequestService.create({
                "data": {"id": id},
                "status": "pending",
                "user_id": current_user.id
            })
            return {"message": "Delete request sent to admin"}, 200

        DriveService.delete(id)
        return {"message": "Drive deleted successfully"}, 200




#/api/drives get,post like its for creating and listing the existing things
class DriveListResource(Resource):


    # students can view drives
    @auth_required("token")
    def get(self):
        all_drives = DriveService.get_all()

        # admin and company see all drives; students only see approved ones
        if current_user.has_role("student"):
            items = [d for d in all_drives if d.status == "approved"]
        else:
            items = all_drives

        return marshal(items, marshal_fields), 200


    # only company can create drives
    @roles_required("company")
    def post(self):

        args = parser.parse_args()

        company = _get_company_for_user()
        if not company:
            return {"message": "Company profile not found"}, 404

        args["company_id"] = company.id

        RequestService.create({
            "data": args,
            "status": "pending",
            "user_id": current_user.id
        })

        return {"message": "Drive creation request sent to admin"}, 200




