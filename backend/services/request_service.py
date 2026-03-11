from model import Request, db
from services.service_errors import ServiceError

model = Request

class RequestService:

    @staticmethod
    def get_all():
        return model.query.all()

    @staticmethod
    def get_by_id(id):
        item = model.query.get(id)
        if not item:
            raise ServiceError("Request not found")
        return item

    @staticmethod
    def create(data):
        item = model(**data)
        db.session.add(item)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ServiceError("Request creation failed")

        return item

    @staticmethod
    def delete(id):
        item = model.query.get(id)

        if not item:
            raise ServiceError("Request not found")

        db.session.delete(item)
        db.session.commit()

        return {"message": "deleted", "id": id}

    @staticmethod
    def update(data):
        item = model.query.get(data["id"])

        if not item:
            raise ServiceError("Request not found")

        for key, value in data.items():
            if key != "id":
                setattr(item, key, value)

        db.session.commit()

        return item