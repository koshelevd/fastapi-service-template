from pydantic import BaseSettings


class Settings(BaseSettings):
    ALEMBIC_SCRIPT_LOCATION: str = 'migrations:runner'

    ALEMBIC_VERSION_LOCATIONS: str = 'migrations:versions'

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    SA_LOGS = False
    LOGGING_LEVEL = 'INFO'
    LOGGING_JSON = True

    class Config:
        env_file_encoding = 'utf-8'

    @property
    def log_config(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }
        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False
            }
        return config
