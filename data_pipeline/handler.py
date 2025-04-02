"""
Handles database operations for countries.
"""

import json
from typing import List

from backend.db.manager import DatabaseManager
from cache.cache import CacheManager


class Handler:
    """
    Handles database operations for countries.
    """

    @staticmethod
    def add_and_update_countries_to_database(
        db_manager: DatabaseManager,
        new_countries: List[dict],
        updated_countries: List[dict],
    ):
        """
        Add the countries to the database.
        Update the countries if they already exist.

        Args:
            db_manager (DatabaseManager): Database manager instance.
            new_countries (List[dict]): List of new countries to add.
            updated_countries (List[dict]): List of countries to update.

        Returns:
            None
        """
        if new_countries:
            print(f"Adding {len(new_countries)} new countries")
            db_manager.bulk_add_countries(new_countries)
        else:
            print("No new countries to add")

        if updated_countries:
            print(f"Updating {len(updated_countries)} countries")
            db_manager.bulk_update_countries(updated_countries)
        else:
            print("No countries to update")

    @staticmethod
    def add_and_update_countries_to_cache(
        cache_manager: CacheManager,
        new_countries: List[dict],
        updated_countries: List[dict],
    ):
        """
        Add the countries to the cache.
        Update the countries if they already exist.

        Args:
            cache_manager (CacheManager): Cache manager instance.
            new_countries (List[dict]): List of new countries to add.
            updated_countries (List[dict]): List of countries to update.

        Returns:
            None
        """
        if new_countries:
            print(f"Adding {len(new_countries)} new countries to cache")
            for country in new_countries:
                cache_manager.set_data(country["name"], json.dumps(country))
        else:
            print("No new countries to add to cache")

        if updated_countries:
            print(f"Updating {len(updated_countries)} countries in cache")
            for country in updated_countries:
                cache_manager.set_data(country["name"], json.dumps(country))
        else:
            print("No countries to update in cache")
