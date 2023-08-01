from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from kafka.errors import KafkaError

from dto.schemas.exception import HandledExceptionSchema, HandledValidationExceptionSchema
from services.errors import (
    AccessDeniedError,
    ApplicationError,
    DatabaseAccessError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


def kafka_error_handler(_: Request, exc: KafkaError) -> JSONResponse:
    schema = HandledExceptionSchema(message="KafkaError", context={"detail": str(exc)})
    return JSONResponse(content=schema.dict(), status_code=500)


def application_error_handler(_: Request, exc: ApplicationError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=exc.status)


def database_access_error_handler(_: Request, exc: DatabaseAccessError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=exc.status)


def object_not_found_error_handler(_: Request, exc: ObjectNotFoundError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=exc.status)


def object_already_exists_error_handler(_: Request, exc: ObjectAlreadyExistsError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=exc.status)


def access_denied_error_handler(_: Request, exc: AccessDeniedError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=exc.status)


def request_validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    exception_schema = HandledValidationExceptionSchema(
        message="Невозможно обработать тело/параметры запроса",
        context=[jsonable_encoder(exc.errors())],
    )
    return JSONResponse(status_code=422, content=exception_schema.dict())
