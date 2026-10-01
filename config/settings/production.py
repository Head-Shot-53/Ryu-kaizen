from .base import *
from .base import env


DEBUG = False


# Production domains
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")


CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=[],
)


# HTTPS proxy configuration
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# Redirect HTTP to HTTPS
SECURE_SSL_REDIRECT = env.bool(
    "DJANGO_SECURE_SSL_REDIRECT",
    default=True,
)


# Secure cookies
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# Prevent browsers from detecting a different content type
SECURE_CONTENT_TYPE_NOSNIFF = True


# Prevent sending the full URL as a referrer to another website
SECURE_REFERRER_POLICY = "same-origin"


# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = env.int(
    "DJANGO_SECURE_HSTS_SECONDS",
    default=31536000,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


# Production email settings will be configured during deployment
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Ryu Kaizen <noreply@example.com>",
)