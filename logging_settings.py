import logging.config
import os


log_config = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": '%(asctime)s - %(levelname)s - %(message)s',
            "datefmt": '%d-%b-%y %H:%M:%S',
        },
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": os.environ.get("LOGGING_PATH", None)
        },
    },
    "loggers": {
        "log": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
        "console": {
            "handlers": ["console_handler"],
            "level": "INFO",
        }
    },
}

logging.config.dictConfig(log_config)
logger = logging.getLogger('log')
console_logger = logging.getLogger('console')
