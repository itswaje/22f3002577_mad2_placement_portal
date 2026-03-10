# interacts with db
from model import PlacementDrive, db
from services.service_errors import ServiceError
from datetime import datetime

class DriveService:

    @staticmethod
    def get_all():
        return PlacementDrive.query.all()

    @staticmethod
    def get_by_id(id):
        item = PlacementDrive.query.get(id)

        if not item:
            raise ServiceError("not found")

        return item
    

    @staticmethod
    def create(data):

        if isinstance(data.get("application_deadline"), str):
            data["application_deadline"] = datetime.strptime(
                data["application_deadline"], "%Y-%m-%d"
            ).date()

        item = PlacementDrive(**data)

        db.session.add(item)
        db.session.commit()

        return item

    @staticmethod
    def get_by_company(company_id):
         return PlacementDrive.query.filter_by(company_id=company_id).all()


    @staticmethod
    def update(data):
        item = PlacementDrive.query.get(data["id"])

        if not item:
            raise ServiceError("not found")

        # convert date string to python date
        if isinstance(data.get("application_deadline"), str):
            data["application_deadline"] = datetime.strptime(
                data["application_deadline"], "%Y-%m-%d"
            ).date()

        for key, value in data.items():
            if key != "id" and hasattr(item, key):
                setattr(item, key, value)

        db.session.commit()

        return item
    
    @staticmethod
    def delete(id):
        item = PlacementDrive.query.get(id)

        if not item:
            raise ServiceError("not found")

        db.session.delete(item)
        db.session.commit()