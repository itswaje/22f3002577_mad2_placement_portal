#creating custome errors it just inherits the exception and creating service error so i know that service error is being thrown 
class ServiceError(Exception):
    def __init__(self, message):
        self.message = message