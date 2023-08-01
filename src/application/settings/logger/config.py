from application.settings.logger.settings import Settings


def make_logger_conf(
    *confs,
    log_level=Settings().LOGGING_LEVEL,
    json_log=Settings().LOGGING_JSON,
):
    fmt = "%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": fmt,
                "datefmt": datefmt,
            },
            "json": {"format": fmt, "datefmt": datefmt, "class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
        },
        "handlers": {
            "default": {
                "level": log_level,
                "formatter": "json" if json_log else "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": log_level, "propagate": False},
        },
    }
    for conf in confs:
        for key in conf.keys():
            config[key].update(conf[key])

    return config
