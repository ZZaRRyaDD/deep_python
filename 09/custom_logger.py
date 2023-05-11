import logging

conf = {
    "version": 1,
    "formatters": {
        "stdout": {
            "format": "%(asctime)s\t%(levelname)s\t[STDOUT]\t%(message)s",
        },
        "main": {
            "format": "%(asctime)s\t%(levelname)s\t[MAIN]\t%(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "stdout",
        },
        "main": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "cache.log",
            "formatter": "main",
        },
    },
    "loggers": {
        "stdout": {
            "level": "DEBUG",
            "handlers": ["stdout",],
        },
        "main": {
            "level": "DEBUG",
            "handlers": ["main",]
        },
    },
}
