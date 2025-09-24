import importlib.util
import pytest
from aieb_evaluation_svc.core.config import settings


class TestProjectStructure:
    """Test the project restructuring changes."""
    
    def test_packages_exist(self):
        """Test that all required packages exist and can be imported."""
        required_packages = [
            "aieb_evaluation_svc.api",
            "aieb_evaluation_svc.services", 
            "aieb_evaluation_svc.schemas",
            "aieb_evaluation_svc.worker",
            "aieb_evaluation_svc.core"
        ]
        
        for package in required_packages:
            spec = importlib.util.find_spec(package)
            assert spec is not None, f"Package {package} should exist"
    
    def test_config_new_location(self):
        """Test that config can be imported from the new core location."""
        # This import should work without error
        from aieb_evaluation_svc.core.config import settings
        
        # Verify settings object exists and has expected attributes
        assert hasattr(settings, 'SERVICE_PORT')
        assert isinstance(settings.SERVICE_PORT, int)
        
        # Verify default value when not overridden
        assert settings.SERVICE_PORT == 8000
    
    def test_old_config_removed(self):
        """Test that the old config location no longer exists."""
        spec = importlib.util.find_spec("aieb_evaluation_svc.config")
        assert spec is None, "Old config path should be removed"
    
    def test_app_starts(self, client):
        """Test that the FastAPI app boots correctly with the new structure."""
        # Use the client fixture from conftest.py to verify app starts
        response = client.get("/openapi.json")
        assert response.status_code == 200, "FastAPI app should boot successfully"
        
        # Verify the response contains OpenAPI schema
        openapi_data = response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
