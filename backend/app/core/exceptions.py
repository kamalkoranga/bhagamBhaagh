from fastapi import HTTPException, status


class AppError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Something went wrong"

    def __init__(self, message: str|None = None):
        super().__init__(
            status_code=self.status_code,
            detail=message or self.default_message
        )

class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Resource not found"

class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    default_message = "Resource already exists"

class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Invalid credentials"

class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "You do not have access to this resource"

class ValidationFailedError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    default_message = "Route failed validation"
