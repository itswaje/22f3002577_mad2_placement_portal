from model import Student, User, db
from services.service_errors import ServiceError


class StudentService:
    ALLOWED_UPDATE_FIELDS = {
        "name",
        "branch",
        "year",
        "cgpa",
        "skills",
        "resume_path",
    }

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
            if key in StudentService.ALLOWED_UPDATE_FIELDS and hasattr(item, key):
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

    @staticmethod
    def blacklist_student(student_id):
        student = Student.query.get(student_id)

        if not student:
            raise ServiceError("Student not found")

        if not student.is_active:
            raise ServiceError("Student already blacklisted")

        student.is_active = False

        user = User.query.get(student.user_id)
        if user:
            user.active = False

        db.session.commit()

        return "Student blacklisted successfully"
