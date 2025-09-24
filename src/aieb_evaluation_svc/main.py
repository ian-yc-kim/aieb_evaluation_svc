import logging

import uvicorn
from aieb_evaluation_svc.app import app
from aieb_evaluation_svc.core.config import settings


# Set up logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    service_port = settings.SERVICE_PORT
    uvicorn.run(app, host="0.0.0.0", port=service_port)


if __name__ == "__main__":
    # Entry point for the application
    main()
