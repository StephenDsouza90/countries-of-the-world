"""
Contains the APIBackend class, which is the main entrypoint for the API backend.
It initializes the FastAPI app instance and the DatabaseManager instance.
It also sets up the routes for the API.
"""

from typing import Optional

from redis import StrictRedis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

from backend.db.manager import DatabaseManager
from backend.api.decorator import handle_exception
from backend.api.handler import RequestHandler
from cache.cache import CacheManager


class APIBackend:
    """
    Main entrypoint for the API backend
    """

    def __init__(self, db_url: str, redis_client: StrictRedis):
        self.app = FastAPI(
            title="Recruiting Test",
            version="0.1.0",
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.db_manager = self._initialize_database_manager(db_url)
        self.cache_manager = self._initialize_cache_manager(redis_client)
        self.request_handler = RequestHandler(self.db_manager, self.cache_manager)
        self._setup_routes()

    def _initialize_database_manager(self, db_url: str) -> DatabaseManager:
        """
        Initialize the database manager

        Args:
            db_url (str): The database URL

        Raises:
            ValueError: If the DB_URL environment variable is not set

        Returns:
            DatabaseManager: The database manager instance
        """
        if not db_url:
            raise ValueError("DB_URL environment variable is not set.")
        manager = DatabaseManager(db_url)
        manager.bootstrap()
        return manager

    def _initialize_cache_manager(self, redis_client: StrictRedis) -> CacheManager:
        """
        Initialize the cache manager

        Args:
            redis_client (StrictRedis): The Redis client

        Returns:
            CacheManager: The cache manager instance
        """
        return CacheManager(redis_client)

    def _setup_routes(self):
        @self.app.get("/")
        async def get_root():
            """
            Show welcome message
            """
            return {"message": "Welcome to the recruiting test backend API."}

        @self.app.get("/countries")
        @handle_exception
        async def get_countries(
            limit: Optional[int] = None,
            sortBy: Optional[str] = Query("name", description="Field to sort by"),
            orderBy: Optional[str] = Query(
                "asc", description="Sort order: 'asc' or 'desc'"
            ),
        ):
            """
            Get a list of countries

            Args:
                limit (Optional[int]): The maximum number of countries to return
                sortBy (Optional[str]): The field to sort by
                orderBy (Optional[str]): The sort order, either 'asc' or 'desc'

            Returns:
                dict: A dictionary containing the list of countries

            Raises:
                ValueError: If the field are not valid
            """
            countries = self.request_handler.get_countries(limit, sortBy, orderBy)
            return {"countries": countries}
