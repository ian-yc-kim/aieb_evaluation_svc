"""FastAPI endpoints for triggering Celery tasks."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from aieb_evaluation_svc.worker.celery_app import add

# Configure logging
logger = logging.getLogger(__name__)

# Create router
celery_tasks_router = APIRouter()


class TaskDispatchResponse(BaseModel):
    """Response model for task dispatch endpoints."""
    task_id: str


@celery_tasks_router.get("/test-celery-task", response_model=TaskDispatchResponse)
async def trigger_test_celery_task(x: int, y: int) -> TaskDispatchResponse:
    """Trigger the Celery add test task.
    
    Args:
        x: First integer to add
        y: Second integer to add
        
    Returns:
        TaskDispatchResponse containing the task ID
        
    Raises:
        HTTPException: If task dispatch fails
    """
    try:
        logger.info(f"Dispatching add task with x={x}, y={y}")
        
        # Dispatch the Celery task
        async_result = add.delay(x, y)
        
        logger.info(f"Task dispatched successfully with ID: {async_result.id}")
        
        return TaskDispatchResponse(task_id=async_result.id)
        
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Failed to dispatch task"
        )
