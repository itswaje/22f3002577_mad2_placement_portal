from model import Student, db
from services.service_errors import ServiceError


class StudentService:

    @staticmethod
    def get_all():
        return Student.query.all()

    @staticmethod
    def get_by_id(id):
        item = Student.query.get(id)

        if not item:
            raise ServiceError("Student not found")

        return item

    @staticmethod
    def create(data):
        item = Student(**data)

        db.session.add(item)
        db.session.commit()

        return item

    @staticmethod
    def update(id, data):
        item = Student.query.get(id)

        if not item:
            raise ServiceError("Student not found")

        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)

        db.session.commit()

        return item

    @staticmethod
    def delete(id):
        item = Student.query.get(id)

        if not item:
            raise ServiceError("Student not found")

        db.session.delete(item)
        db.session.commit()
