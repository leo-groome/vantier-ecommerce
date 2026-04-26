"""Custom exceptions and FastAPI exception handlers for Vantier backend."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for all application-level errors.

    Args:
        detail: Human-readable error message.
        status_code: HTTP status code to return.
        error_code: Machine-readable error code for client handling.
    """

    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "BAD_REQUEST",
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(detail)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND, "NOT_FOUND")


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Authentication required") -> None:
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED")


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Insufficient permissions") -> None:
        super().__init__(detail, status.HTTP_403_FORBIDDEN, "FORBIDDEN")


class ConflictException(AppException):
    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(detail, status.HTTP_409_CONFLICT, "CONFLICT")


class MarginViolationException(AppException):
    """Raised when a pricing change would breach the 50% margin floor."""

    def __init__(self, detail: str = "Price would violate 50% margin floor") -> None:
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY, "MARGIN_VIOLATION")


class StockInsufficientException(AppException):
    def __init__(self, detail: str = "Insufficient stock for requested quantity") -> None:
        super().__init__(detail, status.HTTP_409_CONFLICT, "STOCK_INSUFFICIENT")


def _error_response(status_code: int, error_code: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error_code, "detail": detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app instance."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return _error_response(exc.status_code, exc.error_code, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "VALIDATION_ERROR",
            str(exc.errors()),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        return _error_response(
            status.HTTP_409_CONFLICT,
            "CONFLICT",
            "A resource with conflicting unique constraints already exists.",
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception: %s | type=%s", exc, type(exc).__name__, exc_info=True)
        return _error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_ERROR",
            "An unexpected error occurred.",
        )
