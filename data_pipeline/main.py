"""
Fetches data from the API.
It adds / updates the data to the database.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_pipeline.client import RestCountriesAPIClient
from data_pipeline.handler import Handler
from internal.db.manager import NoSQLDatabaseManager
from internal.cache.client import RedisClient
from internal.cache.cache import CacheManager


class DataPipelineOrchestrator:
    """
    Orchestrates the data pipeline process.
    """

    def __init__(self, db_manager: NoSQLDatabaseManager, cache_manager: CacheManager):
        """
        Initialize the DataPipelineOrchestrator with database and cache managers.

        Args:
            db_manager (NoSQLDatabaseManager): Database manager instance.
            cache_manager (CacheManager): Cache manager instance.
        """
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def main(self):
        """
        Main method to orchestrate the data pipeline.
        """
        countries = RestCountriesAPIClient.fetch_countries()
        handler = Handler(self.db_manager, self.cache_manager)
        handler.process_countries(countries)


if __name__ == "__main__":
    db_url = os.getenv("MANGO_DB_URL")
    if not db_url:
        raise ValueError("DB_URL environment variable is not set.")

    database_manager = NoSQLDatabaseManager(db_url)
    database_manager.bootstrap()

    redis_client = RedisClient().get_client()
    cache_manager = CacheManager(redis_client)

    DataPipelineOrchestrator(database_manager, cache_manager).main()
