import time
import logging
from typing import Union

from celery import Celery

from aieb_evaluation_svc.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Celery application
celery_app = Celery(
    "aieb_evaluation_svc",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BROKER_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task
def add(x: int, y: int) -> int:
    """Simple test task that adds two numbers after a simulated delay.
    
    Args:
        x: First integer to add
        y: Second integer to add
        
    Returns:
        Sum of x and y
        
    Raises:
        Exception: If any error occurs during processing
    """
    try:
        logger.info(f"Processing add task with x={x}, y={y}")
        
        # Simulate some processing time
        time.sleep(0.1)
        
        result = x + y
        logger.info(f"Add task completed with result={result}")
        
        return result
        
    except Exception as e:
        logger.error(e, exc_info=True)
        raise


__all__ = ["celery_app", "add"]
