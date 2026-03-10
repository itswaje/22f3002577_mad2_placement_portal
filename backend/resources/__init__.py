from flask_restful import Api
from flask import Blueprint
# import auth blueprint
from resources.auth_resource import auth_bp
# import all resources
from .drive_resource import DriveResource,DriveListResource
from .company_resource import CompanyDrivesResource
from .student_resource import StudentResource, StudentListResource
from .company_resource import CompanyResource, CompanyListResource
from .application_resource import ApplicationResource, ApplicationListResource, DriveApplicationsResource, StudentApplicationsResource
from .admin_resource import AdminDashboardResource,CompanyApproveResource,CompanyRejectResource,DriveApproveResource,DriveRejectResource
# main api blueprint
api_bp= Blueprint("api",__name__,url_prefix="/api")
# attach flask-restful
api = Api(api_bp)
# DRIVE APIs
api.add_resource(DriveListResource,"/drives")
api.add_resource(DriveResource,"/drives/<int:id>")


# STUDENT APIs
api.add_resource(StudentListResource, "/students")
api.add_resource(StudentResource, "/students/<int:id>")
# COMPANY APIs
api.add_resource(CompanyListResource, "/companies")
api.add_resource(CompanyResource, "/companies/<int:id>")
api.add_resource(CompanyDrivesResource, "/companies/<int:id>/drives")
# APPLICATION APIs
api.add_resource(ApplicationListResource, "/applications")
api.add_resource(ApplicationResource, "/applications/<int:id>")
api.add_resource(DriveApplicationsResource, "/drives/<int:drive_id>/applications")#shows no of application a drive got 
api.add_resource(StudentApplicationsResource, "/students/<int:student_id>/applications")#shows all drives that student applied to 
# ADMIN APIs
api.add_resource(AdminDashboardResource, "/admin/dashboard")
api.add_resource(CompanyApproveResource, "/admin/companies/<int:id>/approve")
api.add_resource(CompanyRejectResource, "/admin/companies/<int:id>/reject")
api.add_resource(DriveApproveResource, "/admin/drives/<int:id>/approve")
api.add_resource(DriveRejectResource, "/admin/drives/<int:id>/reject")
