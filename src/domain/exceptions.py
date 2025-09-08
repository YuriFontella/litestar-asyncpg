from __future__ import annotations


class DomainError(Exception):
    """Base error for domain/application layer.

    Carries an HTTP-like status code for mapping at the presentation layer,
    without importing framework exceptions.
    """

    status_code: int = 400

    def __init__(self, message: str = "", *, status_code: int | None = None) -> None:
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class UserAlreadyExists(DomainError):
    status_code = 409


class InvalidCredentials(DomainError):
    status_code = 401


class ResourceNotFound(DomainError):
    status_code = 404


class OperationFailed(DomainError):
    status_code = 400
