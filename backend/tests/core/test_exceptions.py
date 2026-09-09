import pytest
from fastapi import status

from app.core.exceptions import (
    AppError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationFailedError,
)


@pytest.mark.parametrize(
    ("exception_class", "expected_status", "expected_message"),
    [
        (
            AppError,
            status.HTTP_400_BAD_REQUEST,
            "Something went wrong",
        ),
        (
            NotFoundError,
            status.HTTP_404_NOT_FOUND,
            "Resource not found",
        ),
        (
            ConflictError,
            status.HTTP_409_CONFLICT,
            "Resource already exists",
        ),
        (
            UnauthorizedError,
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
        ),
        (
            ForbiddenError,
            status.HTTP_403_FORBIDDEN,
            "You do not have access to this resource",
        ),
        (
            ValidationFailedError,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Route failed validation",
        ),
    ],
)
def test_exception_defaults(
    exception_class,
    expected_status,
    expected_message,
):
    error = exception_class()

    assert error.status_code == expected_status
    assert error.detail == expected_message


def test_exception_accepts_custom_message():
    error = NotFoundError("User not found")

    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert error.detail == "User not found"
