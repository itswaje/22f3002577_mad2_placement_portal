from model import Company, User,db
from services.service_errors import ServiceError


class CompanyService:

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
            if key != "id" and hasattr(item, key):
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

        # activate user account so they can log in
        user = User.query.get(company.user_id)
        if user:
            user.active = True

        db.session.commit()

        return "Company approved successfully"

        
    @staticmethod
    def delete(id):
        item = Company.query.get(id)

        if not item:
            raise ServiceError("Company not found")

        db.session.delete(item)
        db.session.commit()