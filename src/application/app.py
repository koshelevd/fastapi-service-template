import logging.config

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from kafka.errors import KafkaError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from application.settings.app import Settings as app_settings
from application.settings.broker import Settings as kafka_settings
from application.settings.db import Settings as db_settings
from application.settings.logger import config, settings
from controllers.dependencies import get_session
from controllers.exception_handlers import (
    access_denied_error_handler,
    application_error_handler,
    database_access_error_handler,
    kafka_error_handler,
    object_already_exists_error_handler,
    object_not_found_error_handler,
    request_validation_error_handler,
)
from dto.schemas.exception import HandledValidationExceptionSchema
from middleware.cors import get_cors_middleware
from services.errors import (
    AccessDeniedError,
    ApplicationError,
    DatabaseAccessError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)

app_settings = app_settings()
db_url = db_settings().get_db_url()
logger_settings = settings.Settings()
kafka_app_settings = kafka_settings()


def setup_dependencies(app: FastAPI) -> None:
    engine = create_async_engine(db_url)
    session = async_sessionmaker(engine, expire_on_commit=False)
    app.dependency_overrides[async_sessionmaker] = lambda: session
    app.dependency_overrides[kafka_settings] = lambda: kafka_app_settings
    app.dependency_overrides[AsyncSession] = get_session


def setup_exception_handlers(app: FastAPI) -> None:
    del app.exception_handlers[RequestValidationError]
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(KafkaError, kafka_error_handler)
    app.add_exception_handler(ObjectNotFoundError, object_not_found_error_handler)
    app.add_exception_handler(ObjectAlreadyExistsError, object_already_exists_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_error_handler)
    app.add_exception_handler(DatabaseAccessError, database_access_error_handler)


def app_setup(app: FastAPI) -> None:
    setup_dependencies(app)
    setup_exception_handlers(app)


def init_app() -> FastAPI:
    log_config = config.make_logger_conf(logger_settings.log_config)
    if not app_settings.DEBUG:
        logging.config.dictConfig(log_config)
    app = FastAPI(
        title="Example service",
        debug=app_settings.DEBUG,
        middleware=[get_cors_middleware(app_settings.CORS_ORIGINS)],
    )
    app.include_router(
        router,
        responses={
            422: {
                "description": "Validation Error",
                "model": HandledValidationExceptionSchema,
            }
        },
    )
    app_setup(app)
    return app
