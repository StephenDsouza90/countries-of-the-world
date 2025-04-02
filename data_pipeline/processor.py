"""
This module contains the processor class for the country data.
"""

import json
from typing import List, Tuple

from backend.db.manager import DatabaseManager
from cache.cache import CacheManager


class Processor:
    """
    Handles processing of country data.
    """

    @staticmethod
    def process(
        countries: List[dict], db_manager: DatabaseManager, cache_manager: CacheManager
    ) -> Tuple[List[dict], List[dict]]:
        """
        Process the countries data.

        Args:
            countries (List[dict]): List of countries data.
            db_manager (DatabaseManager): Database manager instance.
            cache_manager (CacheManager): Cache manager instance.

        Returns:
            Tuple[List[dict], List[dict]]: Tuple containing new countries and updated countries.

        Raises:
            KeyError: If the country data is missing required fields.
        """
        new_countries = []
        updated_countries = []

        for country in countries:
            try:
                # Extract the data
                name = country["name"]["common"]
                region = country["region"]
                population = country["population"]
                area = country["area"]
                population_density = population / area

                # Check if the country is already in the cache
                match = cache_manager.get_data(name)
                match = json.loads(match) if match else None

                # Add / Update the country
                match match:
                    case None:
                        new_countries.append(
                            {
                                "name": name,
                                "region": region,
                                "population": population,
                                "area": area,
                                "population_density": population_density,
                            }
                        )

                    case _ if (
                        population != match["population"] or area != match["area"]
                    ):
                        updated_countries.append(
                            {
                                "name": name,
                                "country": match,
                                "population": population,
                                "area": area,
                                "population_density": population / area,
                            }
                        )

            except KeyError as error:
                raise KeyError(f"Couldn't process country: {error}")

        return new_countries, updated_countries
