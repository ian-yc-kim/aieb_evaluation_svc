"""Tests to validate README.md contains proper async task setup documentation."""

import pytest
from pathlib import Path


def test_readme_contains_required_async_setup_instructions():
    """Test that README.md contains all required instructions for Redis/Celery setup."""
    # Read the README file
    readme_path = Path("README.md")
    assert readme_path.exists(), "README.md file should exist"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Test for Redis broker URL configuration
    assert "REDIS_BROKER_URL" in readme_content, "README should mention REDIS_BROKER_URL configuration"
    assert "redis://localhost:6379/0" in readme_content, "README should include example Redis URL"
    
    # Test for Celery worker start command
    expected_worker_command = "poetry run celery -A aieb_evaluation_svc.worker.celery_app worker -l info"
    assert expected_worker_command in readme_content, "README should contain the exact Celery worker start command"
    
    # Test for FastAPI app start instructions
    assert "uvicorn aieb_evaluation_svc.app:app" in readme_content, "README should include uvicorn command for starting FastAPI"
    
    # Test for async task endpoint testing instructions
    assert "/api/test-celery-task" in readme_content, "README should mention the test Celery task endpoint"
    
    # Test for curl command example
    assert "curl" in readme_content, "README should include curl command example for testing"
    assert "x=2&y=3" in readme_content, "README should include specific test parameters"
    
    # Test that both FastAPI and Celery worker read same .env configuration
    assert "Both the FastAPI application and Celery worker read the same `.env` file" in readme_content, \
        "README should explain that both services use same .env file"
    
    # Test for Docker Redis setup instructions
    assert "docker run -d --name redis -p 6379:6379 redis:7-alpine" in readme_content, \
        "README should include Docker command for running Redis"


def test_readme_structure_has_async_sections():
    """Test that README.md has proper sections for async setup."""
    readme_path = Path("README.md")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for key section headers
    assert "## Running the Services" in readme_content, "README should have 'Running the Services' section"
    assert "### 1. Start Redis" in readme_content, "README should have Redis setup section"
    assert "### 2. Start the FastAPI Application" in readme_content, "README should have FastAPI setup section"
    assert "### 3. Start the Celery Worker" in readme_content, "README should have Celery worker setup section"
    assert "## Testing Asynchronous Tasks" in readme_content, "README should have async task testing section"
    
    # Check for environment configuration section
    assert "## Environment Configuration" in readme_content, "README should have environment configuration section"
    assert "### Required Environment Variables" in readme_content, "README should have required environment variables section"
    assert "### Setting Environment Variables in Shell" in readme_content, "README should have shell environment setup section"


def test_readme_contains_troubleshooting_notes():
    """Test that README.md includes helpful troubleshooting notes."""
    readme_path = Path("README.md")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for alternative Celery command with explicit attribute
    assert "celery_app:celery_app" in readme_content, \
        "README should include alternative Celery command for compatibility"
    
    # Check for task result retrieval instructions
    assert "AsyncResult" in readme_content, "README should include instructions for retrieving task results"
    assert "from celery.result import AsyncResult" in readme_content, \
        "README should include Python code for result retrieval"
