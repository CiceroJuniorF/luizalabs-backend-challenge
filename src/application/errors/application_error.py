from src.application.errors.application_errors_enum import ApplicationErrors


class ApplicationError(Exception):
    def __init__(self, application_error: ApplicationErrors, message: str):
        self.message = message
        self.error: ApplicationErrors = application_error
        super().__init__(message)
