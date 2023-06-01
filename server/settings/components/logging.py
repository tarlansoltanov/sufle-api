LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] : {levelname} : {module} : {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{asctime}] : {levelname} : {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "information": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./logs/django/all.log",
            "formatter": "simple",
        },
        "warnings": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "./logs/django/warning.log",
            "formatter": "simple",
        },
        "errors": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "./logs/django/error.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["information", "warnings", "errors", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
