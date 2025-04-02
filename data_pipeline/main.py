"""
Fetches data from the API.
It adds / updates the data to the database.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_pipeline.client import RestCountriesAPIClient
from backend.db.manager import DatabaseManager
from data_pipeline.processor import Processor
from data_pipeline.handler import Handler
from cache.client import redis_client
from cache.cache import CacheManager


class DataPipelineOrchestrator:
    """
    Orchestrates the data pipeline process.
    """

    def __init__(self, db_manager: DatabaseManager, cache_manager: CacheManager):
        """
        Initialize the DataPipelineOrchestrator with database and cache managers.

        Args:
            db_manager (DatabaseManager): Database manager instance.
            cache_manager (CacheManager): Cache manager instance.
        """
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def main(self):
        """
        Main method to orchestrate the data pipeline.
        """
        countries = RestCountriesAPIClient.fetch_countries()
        # countries = [
        #     {
        #         "name": {"common": "Country1"},
        #         "region": "Region1",
        #         "population": 1000000,
        #         "area": 100000,
        #     },
        #     {
        #         "name": {"common": "Country2"},
        #         "region": "Region2",
        #         "population": 2000000,
        #         "area": 200000,
        #     },
        # ]
        new_countries, updated_countries = Processor.process(
            countries, self.db_manager, self.cache_manager
        )
        Handler.add_and_update_countries_to_database(
            self.db_manager, new_countries, updated_countries
        )
        Handler.add_and_update_countries_to_cache(
            self.cache_manager, new_countries, updated_countries
        )


if __name__ == "__main__":
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL environment variable is not set.")

    database_manager = DatabaseManager(db_url)
    database_manager.bootstrap()

    cache_manager = CacheManager(redis_client)

    DataPipelineOrchestrator(database_manager, cache_manager).main()
