"""Integration tests for Celery task endpoints."""

import pytest
from unittest.mock import Mock


class DummyAsyncResult:
    """Mock Celery AsyncResult for testing."""
    def __init__(self, task_id: str):
        self.id = task_id


class DummyTask:
    """Mock Celery task for testing."""
    def __init__(self):
        self.call_args = None
        
    def delay(self, x: int, y: int) -> DummyAsyncResult:
        """Mock delay method that captures arguments."""
        self.call_args = (x, y)
        return DummyAsyncResult("test-task-123")


def test_trigger_test_celery_task_success(client, monkeypatch):
    """Test successful Celery task dispatch via API endpoint."""
    # Import the module where the task is used
    from aieb_evaluation_svc.api import celery_tasks as module
    
    # Create a mock task
    mock_task = DummyTask()
    
    # Patch the task at the usage site
    monkeypatch.setattr(module, "add", mock_task)
    
    # Call the endpoint
    response = client.get("/api/test-celery-task", params={"x": 5, "y": 7})
    
    # Verify response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == "test-task-123"
    
    # Verify the task was called with correct arguments
    assert mock_task.call_args == (5, 7)


def test_trigger_test_celery_task_negative_numbers(client, monkeypatch):
    """Test Celery task dispatch with negative numbers."""
    from aieb_evaluation_svc.api import celery_tasks as module
    
    mock_task = DummyTask()
    monkeypatch.setattr(module, "add", mock_task)
    
    response = client.get("/api/test-celery-task", params={"x": -3, "y": -5})
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["task_id"] == "test-task-123"
    assert mock_task.call_args == (-3, -5)


def test_trigger_test_celery_task_missing_parameters(client):
    """Test API endpoint with missing required parameters."""
    # Missing y parameter
    response = client.get("/api/test-celery-task", params={"x": 5})
    assert response.status_code == 422  # Validation error
    
    # Missing x parameter
    response = client.get("/api/test-celery-task", params={"y": 7})
    assert response.status_code == 422  # Validation error
    
    # Missing both parameters
    response = client.get("/api/test-celery-task")
    assert response.status_code == 422  # Validation error


def test_trigger_test_celery_task_invalid_parameters(client):
    """Test API endpoint with invalid parameter types."""
    # Non-integer parameters
    response = client.get("/api/test-celery-task", params={"x": "invalid", "y": "also_invalid"})
    assert response.status_code == 422  # Validation error
    
    # Float parameters (should be converted to int by FastAPI)
    response = client.get("/api/test-celery-task", params={"x": "5.5", "y": "7.2"})
    assert response.status_code == 422  # Validation error for non-convertible floats


def test_trigger_test_celery_task_exception_handling(client, monkeypatch):
    """Test API endpoint exception handling when task dispatch fails."""
    from aieb_evaluation_svc.api import celery_tasks as module
    
    # Create a mock that raises an exception
    def failing_delay(x, y):
        raise Exception("Celery connection failed")
    
    mock_task = Mock()
    mock_task.delay = failing_delay
    
    monkeypatch.setattr(module, "add", mock_task)
    
    response = client.get("/api/test-celery-task", params={"x": 5, "y": 7})
    
    # Should return 500 error due to task dispatch failure
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Failed to dispatch task"
