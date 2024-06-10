import os

from .base import *  # noqa: F401, F403

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # noqa: F405
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "mydatabase"),
        "USER": os.environ.get("DATABASE_USER", "myuser"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "mypassword"),
        "HOST": os.environ.get("DATABASE_HOST", "db"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
