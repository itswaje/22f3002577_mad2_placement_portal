from model import Company, User, PlacementDrive, db
from services.service_errors import ServiceError


class CompanyService:
    ALLOWED_UPDATE_FIELDS = {
        "company_name",
        "industry",
        "location",
        "website",
        "hr_contact",
    }

    @staticmethod
    def _set_drive_statuses_for_company(company_id, status):
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()
        for drive in drives:
            # Preserve closed drives; all active ones follow company lifecycle.
            if drive.status != "closed":
                drive.status = status

    @staticmethod
    def get_all():
        return Company.query.all()

    @staticmethod
    def get_by_id(id):
        item = Company.query.get(id)

        if not item:
            raise ServiceError("Company not found")

        return item

    @staticmethod
    def create(data):
        item = Company(**data)

        db.session.add(item)
        db.session.commit()

        return item

    @staticmethod
    def update(id,data):
        item = Company.query.get(id)

        if not item:
            raise ServiceError("Company not found")

        for key, value in data.items():
            if key in CompanyService.ALLOWED_UPDATE_FIELDS and hasattr(item, key):
                setattr(item, key, value)

        db.session.commit()

        return item

    
    @staticmethod
    def approve_company(company_id):

        company = Company.query.get(company_id)

        if not company:
            raise ServiceError("Company not found")

        if company.status == "approved":
            raise ServiceError("Company already approved")

        company.status = "approved"
        CompanyService._set_drive_statuses_for_company(company.id, "approved")

        # activate user account so they can log in
        user = User.query.get(company.user_id)
        if user:
            user.active = True

        db.session.commit()

        return "Company approved successfully"

    @staticmethod
    def blacklist_company(company_id):

        company = Company.query.get(company_id)

        if not company:
            raise ServiceError("Company not found")

        if company.status == "blacklisted":
            raise ServiceError("Company already blacklisted")

        company.status = "blacklisted"
        CompanyService._set_drive_statuses_for_company(company.id, "cancelled")

        user = User.query.get(company.user_id)
        if user:
            user.active = False

        db.session.commit()

        return "Company blacklisted successfully"

        
    @staticmethod
    def delete(id):
        item = Company.query.get(id)

        if not item:
            raise ServiceError("Company not found")

        db.session.delete(item)
        db.session.commit()