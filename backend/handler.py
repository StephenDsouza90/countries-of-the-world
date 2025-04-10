"""
Request handler for the API.
This module handles the request processing and data retrieval from the database and cache.
"""

import os
import base64
import json
from typing import List

from internal.db.manager import NoSQLDatabaseManager
from internal.cache.cache import CacheManager


class RequestHandler:
    """
    Handles requests to the API.
    This class is responsible for processing requests, interacting with the database,
    and managing the cache.
    """

    def __init__(self, db_manager: NoSQLDatabaseManager, cache_manager: CacheManager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def _extract_country_data(self, country: dict) -> dict:
        """
        Extracts relevant data from the country object.

        Args:
            country (dict): The country object.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        return {
            "country_name": country["country_name"],
            "population_density": country["population_density"],
            "area": country["area"],
            "population": country["population"],
            "region": country["region"],
        }

    def _extract_image_data(self, image: dict) -> dict:
        """
        Extracts relevant data from the country object.

        Args:
            country (dict): The country object.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        return {
            "image_id": image["image_id"],
            "title": image["title"],
            "description": image["description"],
        }

    def _get_file_path(self, country_name: str, image_id: str) -> str:
        """
        Get the file path for the image.

        Args:
            country_name (str): The name of the country.
            image_id (str): The ID of the image.

        Returns:
            str: The file path for the image.
        """
        return f"/assets/{country_name}/images/{image_id}.jpg"

    def _create_random_image_id(self) -> str:
        """
        Create a random image ID.

        Returns:
            str: A random image ID.
        """
        return os.urandom(16).hex()

    def get_countries(self, limit: int, sort_by: str, order_by: int) -> List[dict]:
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
            return json.loads(cached_data)

        # If not in cache, fetch from the database
        countries = self.db_manager.get_countries(limit, sort_by, order_by)
        countries = [self._extract_country_data(country) for country in countries]

        # Serialize the result and store it in the cache
        self.cache_manager.set_data(cache_key, json.dumps(countries))

        return countries

    def get_country(self, country_name: str) -> dict:
        """
        Get a country by name from the database or cache.

        Args:
            country_name (str): The name of the country to retrieve.

        Returns:
            Country: A Country object.
        """
        cache_key = f"country:{country_name}"

        # Check if the data is in the cache
        cached_data = self.cache_manager.get_dict_data(cache_key)
        if cached_data:
            return cached_data

        # If not in cache, fetch from the database
        country = self.db_manager.get_country(country_name)
        country = self._extract_country_data(country)

        # Serialize the result and store it in the cache
        self.cache_manager.set_dict_data(cache_key, country)

        return country

    def upload_image(
        self, country_name: str, file: bytes, title: str, description: str
    ) -> str:
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
            str: The ID of the uploaded image.
        """
        image_id = self._create_random_image_id()

        file_path = self._get_file_path(country_name, image_id)

        image = {
            "image_id": image_id,
            "country_name": country_name,
            "title": title,
            "description": description,
            "file_path": file_path,
        }

        # Save image metadata to the database
        self.db_manager.add_image(image_id, image)

        # Save the image file to the file system
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file)

        # Update the cache for the country's images
        cache_key = f"images:{country_name}"
        cached_images = self.cache_manager.get_data(cache_key)
        if cached_images:
            cached_images = json.loads(cached_images)
        else:
            cached_images = []

        # Add the new image metadata to the cache
        cached_images.append(
            {
                "image_id": image_id,
                "title": title,
                "description": description,
                "file": base64.b64encode(file).decode("utf-8"),
            }
        )

        # Serialize and update the cache
        self.cache_manager.set_data(cache_key, json.dumps(cached_images))

        return image_id

    def get_images(self, country_name: str) -> List[dict]:
        """
        Get images for a country from the database or cache.

        Args:
            country_name (str): The name of the country.

        Returns:
            List[bytes]: A list of image files.
        """
        cache_key = f"images:{country_name}"

        # Check if the data is in the cache
        cached_data = self.cache_manager.get_data(cache_key)
        if cached_data:
            return json.loads(cached_data)

        # Get images meta data from the database
        images_meta_data = self.db_manager.get_images(country_name)
        images_meta_data = [
            self._extract_image_data(image) for image in images_meta_data
        ]

        # Get images from the file system
        images = []

        for image in images_meta_data:
            file_path = self._get_file_path(country_name, image["image_id"])
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file = f.read()
                    image["file"] = base64.b64encode(file).decode("utf-8")
                    images.append(image)

        # Serialize the result and store it in the cache
        self.cache_manager.set_data(cache_key, json.dumps(images))

        return images
