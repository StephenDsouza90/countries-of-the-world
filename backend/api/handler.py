"""
Request handler for the API.
This module handles the request processing and data retrieval from the database and cache.
"""

import json
from typing import List, Optional

from backend.db.manager import DatabaseManager
from backend.db.model import Country
from cache.cache import CacheManager


class RequestHandler:
    """
    Handles requests to the API.
    This class is responsible for processing requests, interacting with the database,
    and managing the cache.
    """

    def __init__(self, db_manager: DatabaseManager, cache_manager: CacheManager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def get_countries(
        self, limit: Optional[int], sort_by: str, order_by: str
    ) -> List[Country]:
        """
        Get a list of countries from the database or cache.

        Args:
            limit (Optional[int]): The maximum number of countries to return.
            sort_by (str): The field to sort by.
            order_by (str): The sort order, either 'asc' or 'desc'.

        Returns:
            List[Country]: A list of Country objects.
        """
        cache_key = f"countries:limit={limit}:sort_by={sort_by}:order_by={order_by}"

        # Check if the data is in the cache
        cached_data = self.cache_manager.get_data(cache_key)
        if cached_data:
            return [Country(**country) for country in json.loads(cached_data)]

        # If not in cache, fetch from the database
        countries = self.db_manager.get_countries(limit, sort_by, order_by)

        # Serialize the result and store it in the cache
        self.cache_manager.set_data(
            cache_key, json.dumps([country.to_dict() for country in countries])
        )

        return countries
