import logging

conf = {
    "version": 1,
    "formatters": {
        "main": {
            "format": "%(asctime)s\t%(levelname)s\t[MAIN]\t%(message)s",
        },
    },
    "handlers": {
        "main": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "cache.log",
            "formatter": "main",
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["main"]
        },
    },
}


class CustomFilter(logging.Filter):
    def filter(self, record):
        return "кеш" not in record.msg
