"""Sanity tests that application settings load and expose expected fields."""

from app.config.settings import Settings, get_settings


def test_get_settings_returns_settings_instance():
    settings = get_settings()

    assert isinstance(settings, Settings)


def test_settings_expose_required_fields():
    settings = get_settings()

    assert settings.app_name
    assert settings.app_version
    assert isinstance(settings.debug, bool)
    assert settings.database_url
    assert settings.secret_key
    assert settings.algorithm
    assert isinstance(settings.access_token_expire_minutes, int)


def test_get_settings_is_cached():
    assert get_settings() is get_settings()
