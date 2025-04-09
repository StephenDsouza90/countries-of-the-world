"""
Handler class for processing country data.
This class is responsible for processing country data,
adding or updating country information in the database,
and managing cache operations.
"""

import json
from typing import List

from internal.db.manager import NoSQLDatabaseManager
from internal.cache.cache import CacheManager


class Handler:
    """
    Handler class for processing country data.
    """

    def __init__(self, db_manager: NoSQLDatabaseManager, cache_manager: CacheManager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def process_countries(self, countries: List[dict]):
        """
        Process a list of countries, adding or updating them in the database and cache.

        Args:
            countries (List[dict]): List of country data dictionaries.

        Returns:
            None
        """
        for country in countries:
            try:
                # name to be used as the key in the cache and database
                name = country["name"]["common"]

                # Extracting population and area
                population = country["population"]
                area = country["area"]

                # Additional fields to be added to the country
                country["country_name"] = name
                country["population_density"] = population / area

                # Check if the country is already in the cache
                match = self.cache_manager.get_data(name)
                match = json.loads(match) if match else None

                if not match:
                    # Check if the country is already in the database
                    match = self.db_manager.get_country(name)

                # Add / Update the country
                match match:
                    case None:
                        # Add to database
                        self.db_manager.add_country(name, country)

                        # Add to cache
                        self.cache_manager.set_data(name, json.dumps(country))

                    case _ if (
                        population != match["population"] or area != match["area"]
                    ):
                        # Update database
                        self.db_manager.update_country(name, country)

                        # Update cache
                        self.cache_manager.set_data(name, json.dumps(country))

            except KeyError as error:
                raise KeyError(f"Couldn't process country: {error}")
