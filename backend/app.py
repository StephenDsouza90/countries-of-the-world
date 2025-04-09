"""
Entry point for the FastAPI application.
It creates an instance of the APIBackend class and uses the FastAPI app instance to serve the API.
"""

import os

from backend.main import APIBackend
from internal.cache.client import RedisClient

db_url = os.getenv("MANGO_DB_URL")
if not db_url:
    raise ValueError("DB_URL environment variable is not set.")

redis_client = RedisClient().get_client()
backend = APIBackend(db_url, redis_client)
app = backend.app
