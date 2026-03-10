from model import Application, db
from services.service_errors import ServiceError


class ApplicationService:

    @staticmethod
    def get_all():
        return Application.query.all()

    @staticmethod
    def get_by_id(id):
        item = Application.query.get(id)

        if not item:
            raise ServiceError("Application not found")

        return item

    @staticmethod
    def create(data):
        item = Application(**data)

        db.session.add(item)
        db.session.commit()

        return item

    @staticmethod
    def update(data):
        item = Application.query.get(data["id"])

        if not item:
            raise ServiceError("Application not found")

        for key, value in data.items():
            if key != "id" and hasattr(item, key):
                setattr(item, key, value)

        db.session.commit()

        return item

    @staticmethod
    def get_by_student(student_id):
        return Application.query.filter_by(student_id=student_id).all()

    @staticmethod
    def get_by_drive(drive_id):
        return Application.query.filter_by(drive_id=drive_id).all()

    @staticmethod
    def delete(id):
        item = Application.query.get(id)

        if not item:
            raise ServiceError("Application not found")

        db.session.delete(item)
        db.session.commit()