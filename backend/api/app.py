"""
Entry point for the FastAPI application.
It creates an instance of the APIBackend class and uses the FastAPI app instance to serve the API.
"""

import os

from backend.api.main import APIBackend
from cache.client import redis_client

db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("DB_URL environment variable is not set.")

backend = APIBackend(db_url, redis_client)
app = backend.app
