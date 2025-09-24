from fastapi import FastAPI

from aieb_evaluation_svc.api.celery_tasks import celery_tasks_router

app = FastAPI(debug=True)

# Include routers
app.include_router(celery_tasks_router, prefix="/api")
