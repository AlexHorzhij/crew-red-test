from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging_config import logger


def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Transaction rolled back."},
    )


def generic_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
