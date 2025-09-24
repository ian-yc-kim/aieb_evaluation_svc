import pytest
from unittest import mock

import aieb_evaluation_svc.core.config as cfg
from aieb_evaluation_svc.core.config import Settings


def test_settings_redis_broker_url_default(monkeypatch):
    """Test that REDIS_BROKER_URL uses default value when env var is not set."""
    # Remove environment variable if it exists
    monkeypatch.delenv("REDIS_BROKER_URL", raising=False)
    
    # Create fresh Settings instance
    settings = Settings()
    
    # Assert default value is used
    assert settings.REDIS_BROKER_URL == "redis://localhost:6379/0"


def test_settings_redis_broker_url_env_override(monkeypatch):
    """Test that REDIS_BROKER_URL can be overridden by environment variable."""
    # Set environment variable to override default
    test_url = "redis://localhost:6380/1"
    monkeypatch.setenv("REDIS_BROKER_URL", test_url)
    
    # Create fresh Settings instance
    settings = Settings()
    
    # Assert environment value is used
    assert settings.REDIS_BROKER_URL == test_url


def test_module_settings_has_redis_broker_url():
    """Test that the module-level settings instance has REDIS_BROKER_URL attribute."""
    # Import config module and verify settings has the attribute
    assert hasattr(cfg.settings, "REDIS_BROKER_URL")
    assert isinstance(cfg.settings.REDIS_BROKER_URL, str)
    # Verify it has some reasonable default value
    assert cfg.settings.REDIS_BROKER_URL.startswith("redis://")
