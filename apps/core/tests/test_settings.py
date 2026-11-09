from django.conf import settings

def test_custom_user_model_is_configured():
    assert settings.AUTH_USER_MODEL == "accounts.User"

def test_global_templates_directory_is_configured():
    templates_directory = settings.BASE_DIR / "templates"

    assert templates_directory in settings.TEMPLATES[0]["DIRS"]

def test_global_static_directory_is_configured():
    static_directory = settings.BASE_DIR / "static"

    assert static_directory in settings.STATICFILES_DIRS