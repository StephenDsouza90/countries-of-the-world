"""
Contains the core functionality of the database.
"""

import sys
import os
from typing import List

from pymongo.cursor import Cursor

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from internal.db.setup import NoSQLBackend


class NoSQLDatabaseManager(NoSQLBackend):
    """
    NoSQLDatabaseManager is used to interact with the NoSQL database.
    """

    KEY_COUNTRY = "country_name"

    def __init__(self, connection_string: str):
        super().__init__(connection_string)

    def add_country(self, key: str, value: dict) -> object:
        """
        Add a country to the NoSQL database.

        Args:
            key: key of the country - name of the country
            value: value of the country - country object

        Returns:
            result: result of the insert operation
        """
        return self.db.countries.insert_one({self.KEY_COUNTRY: key, **value})

    def update_country(self, key: str, value: dict) -> object:
        """
        Update a country in the NoSQL database.

        Args:
            key: key of the country - name of the country
            value: value of the country - country object

        Returns:
            result: result of the update operation
        """
        return self.db.countries.update_one({self.KEY_COUNTRY: key}, {"$set": value})

    def get_countries(self, limit: int, sort_by: str, order_by: int) -> List[Cursor]:
        """
        Get a list of countries from the NoSQL database.

        Args:
            limit: maximum number of countries to return
            sort_by: field to sort by
            order_by: sort order - asc or desc

        Returns:
            countries: list of countries
        """
        return list(self.db.countries.find().limit(limit).sort(sort_by, order_by))

    def get_country(self, key: str) -> dict:
        """
        Get a country from the NoSQL database.

        Args:
            key: key of the country - name of the country

        Returns:
            country: country object
        """
        return self.db.countries.find_one({self.KEY_COUNTRY: key})

    def add_image(self, key: str, value: dict) -> object:
        """
        Add an image to the NoSQL database.

        Args:
            key: key of the country - name of the country
            value: value of the image - image object

        Returns:
            result: result of the insert operation
        """
        return self.db.images.insert_one({self.KEY_COUNTRY: key, **value})

    def get_images(self, key: str) -> List[Cursor]:
        """
        Get a list of images from the NoSQL database.

        Args:
            key: key of the country - name of the country

        Returns:
            images: list of images
        """
        return list(self.db.images.find({self.KEY_COUNTRY: key}))
