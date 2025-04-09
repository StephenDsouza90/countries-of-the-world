"""
Contains the APIBackend class, which is the main entrypoint for the API backend.
It initializes the FastAPI app instance and the SQLDatabaseManager instance.
It also sets up the routes for the API.
"""

from typing import Optional

from redis import StrictRedis
from fastapi import FastAPI, Query, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from internal.db.manager import NoSQLDatabaseManager
from backend.decorator import handle_exception
from backend.handler import RequestHandler
from internal.cache.cache import CacheManager


class APIBackend:
    """
    Main entrypoint for the API backend
    """

    def __init__(self, db_url: str, redis_client: StrictRedis):
        self.app = FastAPI(
            title="Countries API",
            description="API for managing countries and their images",
            version="0.1.0",
            swagger_ui_parameters={"syntaxHighlight": False},
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.db_manager = self._initialize_database_manager(db_url)
        self.cache_manager = self._initialize_cache_manager(redis_client)
        self.request_handler = RequestHandler(self.db_manager, self.cache_manager)
        self._setup_routes()

    def _initialize_database_manager(self, db_url: str) -> NoSQLDatabaseManager:
        """
        Initialize the database manager

        Args:
            db_url (str): The database URL

        Raises:
            ValueError: If the DB_URL environment variable is not set

        Returns:
            NoSQLDatabaseManager: The database manager instance
        """
        if not db_url:
            raise ValueError("DB_URL environment variable is not set.")
        manager = NoSQLDatabaseManager(db_url)
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
        @self.app.get("/countries")
        @handle_exception
        async def get_countries(
            limit: Optional[int] = Query(
                250, description="Maximum number of countries to return"
            ),
            sortBy: Optional[str] = Query(
                "country_name", description="Field to sort by"
            ),
            orderBy: Optional[str] = Query(
                "1", description="Sort order: 1 for asc or -1 for desc"
            ),
        ):
            """
            Get a list of countries

            Args:
                limit (Optional[int]): The maximum number of countries to return
                sortBy (Optional[str]): The field to sort by
                orderBy (Optional[int]): The sort order, either 1 'asc' or -1 'desc'

            Returns:
                dict: A dictionary containing the list of countries

            Raises:
                ValueError: If the field are not valid
            """
            countries = self.request_handler.get_countries(limit, sortBy, int(orderBy))
            return {"countries": countries}

        @self.app.get("/countries/{countryName}")
        @handle_exception
        async def get_country(countryName: str):
            """
            Get a country by name

            Args:
                country_name (str): The name of the country to retrieve

            Returns:
                dict: A dictionary containing the country data

            Raises:
                ValueError: If the field are not valid
            """
            country = self.request_handler.get_country(countryName)
            return {"country": country}

        @self.app.post("/countries/{countryName}/images")
        @handle_exception
        async def upload_image(
            countryName: str,
            file: UploadFile = File(...),
            title: str = Form(...),
            description: str = Form(...),
        ):
            """
            Upload an image for a country

            Args:
                country_name (str): The name of the country
                file (UploadFile): The image file to upload
                title (str): The title of the image
                description (str): The description of the image

            Returns:
                dict: A dictionary containing the result of the upload
            """
            file_content = await file.read()
            result = self.request_handler.upload_image(
                countryName, file_content, title, description
            )
            return {"result": result}

        @self.app.get("/countries/{countryName}/images")
        @handle_exception
        async def get_images(countryName: str):
            """
            Get images for a country

            Args:
                country_name (str): The name of the country

            Returns:
                dict: A dictionary containing the list of images
            """
            images = self.request_handler.get_images(countryName)
            return {"images": images}

        @self.app.get("/health")
        @handle_exception
        async def health_check():
            """
            Health check endpoint

            Returns:
                dict: A dictionary containing the health status
            """
            return {"status": "ok"}
