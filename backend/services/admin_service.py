from model import Student, Company, PlacementDrive,Request,db
from .service_errors import ServiceError

class AdminService:

    @staticmethod
    def dashboard():
        students = Student.query.count()
        companies = Company.query.count()
        drives = PlacementDrive.query.count()

        return {
            "students": students,
            "companies": companies,
            "drives": drives
        }
    @staticmethod
    def reject_company(company_id):

        company = Company.query.get(company_id)

        if not company:
            raise ServiceError("Company not found")

        if company.status == "rejected":
            raise ServiceError("Company already rejected")

        company.status = "rejected"

        db.session.commit()

        return "Company rejected successfully"
    
    @staticmethod
    def approve_drive(request_id):
        from services.drive_service import DriveService

        req = Request.query.get(request_id)

        if not req:
            raise ServiceError("Request not found")

        if req.status == "approved":
            raise ServiceError("Request already approved")

        drive_data = dict(req.data)
        drive_data["status"] = "approved"
        DriveService.create(drive_data)

        req.status = "approved"
        db.session.commit()

        return "Drive approved successfully"
    
    @staticmethod
    def reject_drive(request_id):

        req = Request.query.get(request_id)

        if not req:
            raise ServiceError("Request not found")

        if req.status == "rejected":
            raise ServiceError("Request already rejected")

        req.status = "rejected"

        db.session.commit()

        return "Drive rejected successfully"