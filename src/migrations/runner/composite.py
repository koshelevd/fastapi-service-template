import logging.config

from alembic.config import CommandLine, Config

from migrations.runner.config import Settings as alembic_settings
from application.settings.db import Settings as db_settings
from application.settings.logger.config import make_logger_conf

db_settings = db_settings()
alembic_settings = alembic_settings()


def make_config():
    config = Config()
    config.set_main_option("script_location", alembic_settings.ALEMBIC_SCRIPT_LOCATION)
    config.set_main_option("version_locations", alembic_settings.ALEMBIC_VERSION_LOCATIONS)
    config.set_main_option("sqlalchemy.url", db_settings.get_db_url(async_mode=False))
    config.set_main_option("file_template", alembic_settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE)
    config.set_main_option("timezone", "UTC")
    return config


def alembic_runner(*args):
    log_config = make_logger_conf(
        alembic_settings.log_config,
        log_level=alembic_settings.LOGGING_LEVEL,
        json_log=alembic_settings.LOGGING_JSON,
    )
    logging.config.dictConfig(log_config)
    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
