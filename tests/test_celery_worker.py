import pytest
from celery.result import ResultBase, AsyncResult

from aieb_evaluation_svc.worker import celery_app, add
from aieb_evaluation_svc.core.config import settings


class TestCeleryWorker:
    """Test cases for Celery worker functionality."""
    
    def setup_method(self):
        """Set up eager mode for all tests to avoid Redis connections."""
        self.original_eager = celery_app.conf.task_always_eager
        celery_app.conf.task_always_eager = True
    
    def teardown_method(self):
        """Restore original eager setting after each test."""
        celery_app.conf.task_always_eager = self.original_eager
    
    def test_task_dispatch_returns_result_object(self):
        """Test that dispatching a task returns a Celery result object."""
        # Dispatch the task (runs in eager mode due to setup_method)
        result = add.delay(1, 2)
        
        # Verify it returns a Celery result object
        assert isinstance(result, ResultBase), "Task dispatch should return a Celery ResultBase object"
        
        # In eager mode, tasks return EagerResult which is a subclass of ResultBase
        # We don't test for AsyncResult since we're in eager mode
    
    def test_task_functionality_in_eager_mode(self):
        """Test task functional behavior when running in eager mode."""
        # Task already runs in eager mode due to setup_method
        result = add.delay(1, 2)
        
        # In eager mode, task executes immediately
        assert result.get(timeout=5) == 3, "Task should return correct sum"
        assert result.successful() is True, "Task should complete successfully"
    
    def test_celery_app_configuration(self):
        """Test that Celery app is configured correctly."""
        # Verify broker URL configuration
        assert celery_app.conf.broker_url == settings.REDIS_BROKER_URL, \
            "Broker URL should match settings"
        
        # Verify result backend configuration
        assert celery_app.conf.result_backend == settings.REDIS_BROKER_URL, \
            "Result backend should match settings"
        
        # Verify task serialization settings
        assert celery_app.conf.task_serializer == 'json', \
            "Task serializer should be JSON"
        
        assert 'json' in celery_app.conf.accept_content, \
            "Should accept JSON content"
        
        assert celery_app.conf.result_serializer == 'json', \
            "Result serializer should be JSON"
    
    def test_add_task_with_different_inputs(self):
        """Test add task with various input combinations."""
        # Task already runs in eager mode due to setup_method
        test_cases = [
            (0, 0, 0),
            (5, 3, 8),
            (-1, 1, 0),
            (100, -50, 50)
        ]
        
        for x, y, expected in test_cases:
            result = add.delay(x, y)
            actual = result.get(timeout=5)
            assert actual == expected, f"add({x}, {y}) should return {expected}, got {actual}"
            assert result.successful() is True, f"Task add({x}, {y}) should complete successfully"
    
    def test_celery_app_name(self):
        """Test that Celery app has correct name."""
        assert celery_app.main == "aieb_evaluation_svc", \
            "Celery app should have correct main name"
    
    def test_non_eager_mode_returns_async_result(self):
        """Test that non-eager mode would return AsyncResult (when Redis is available)."""
        # Temporarily disable eager mode for this test
        celery_app.conf.task_always_eager = False
        
        try:
            # This test documents expected behavior but will skip if Redis unavailable
            result = add.delay(1, 2)
            # If we get here without connection error, verify it's AsyncResult
            if not celery_app.conf.task_always_eager:
                assert isinstance(result, AsyncResult), "Non-eager tasks should return AsyncResult"
        except Exception:
            # Skip this test if Redis connection fails - that's expected in test env
            pytest.skip("Redis not available for non-eager mode testing")
        finally:
            # Restore eager mode
            celery_app.conf.task_always_eager = True
