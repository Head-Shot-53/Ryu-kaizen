from .base import *
from .base import env


DEBUG = env.bool(
    "DJANGO_DEBUG",
    default=True,
)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
    ],
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": env("POSTGRES_PORT"),
    }
}


# Emails are displayed in the terminal during development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Development email sender
DEFAULT_FROM_EMAIL = "Ryu Kaizen <dev@localhost>"