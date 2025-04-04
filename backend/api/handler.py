"""
Request handler for the API.
This module handles the request processing and data retrieval from the database and cache.
"""

import os
import base64
import json
from typing import List, Optional

from backend.db.manager import DatabaseManager
from backend.db.model import Country, Image
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

    def get_country(self, country_name: str) -> Country:
        """
        Get a country by name from the database or cache.

        Args:
            country_name (str): The name of the country to retrieve.

        Returns:
            Country: A Country object.
        """
        cache_key = f"country:{country_name}"

        # Check if the data is in the cache
        cached_data = self.cache_manager.get_data(cache_key)
        if cached_data:
            return Country(**json.loads(cached_data))

        # If not in cache, fetch from the database
        country = self.db_manager.get_country(country_name)

        # Serialize the result and store it in the cache
        self.cache_manager.set_data(cache_key, json.dumps(country.to_dict()))

        return country

    def upload_image(
        self, country_name: str, file: bytes, title: str, description: str
    ) -> dict:
        """
        Upload an image for a country.
        This method handles the image upload process, including saving the file
        to the file system and saving the meta data to the database.

        Args:
            country_name (str): The name of the country.
            file (UploadFile): The image file to upload.
            title (str): The title of the image.
            description (str): The description of the image.

        Returns:

        """
        # Save the meta data to the database
        image = Image(
            country_name=country_name,
            title=title,
            description=description,
        )
        image_id = self.db_manager.add_image_meta_data(image)

        # Save the file to the file system
        file_path = f"/assets/{country_name}/images/{image_id}.jpg"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file)

        # TODO: Do something with the cache

        return image_id

    def get_images(self, country_name: str) -> List[dict]:
        """
        Get images for a country from the database or cache.

        Args:
            country_name (str): The name of the country.

        Returns:
            List[bytes]: A list of image files.
        """
        # Get images meta data from the database
        images_meta_data = self.db_manager.get_images_meta_data(country_name)

        # Get images from the file system
        images = []

        for image in images_meta_data:
            d = {}

            file_path = f"/assets/{country_name}/images/{image.id}.jpg"

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file = f.read()

                    encoded_file = base64.b64encode(file).decode("utf-8")

                    d["file"] = encoded_file
                    d["title"] = image.title
                    d["description"] = image.description
                    images.append(d)

        # TODO: Do something with the cache

        return images
