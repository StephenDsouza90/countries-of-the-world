"""
This module provides functions to interact with a Redis cache.
It includes functions to set and get data in the cache.
"""


class CacheManager:
    """
    A class to interact with a Redis cache, providing methods to set and get data.
    """

    def __init__(self, client):
        """
        Initialize the CacheManager with a Redis client.

        Args:
            client: A pre-configured Redis client instance.
        """
        self.client = client

    def set_data(self, key: str, value: any) -> bool:
        """
        Set data in Redis cache with a specified key and value.

        Args:
            key (str): The key under which the value will be stored.
            value (str): The value to be stored in the cache.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.client.set(key, value, ex=60 * 60 * 24)  # Set expiration to 1 day
            return True
        except Exception as e:
            print(f"Error setting data in cache: {e}")
            return False

    def get_data(self, key: str) -> any:
        """
        Get data from Redis cache using a specified key.

        Args:
            key (str): The key for which the value is to be retrieved.

        Returns:
            str: The value associated with the key, or None if an error occurs.
        """
        try:
            value = self.client.get(key)
            return value
        except Exception as e:
            print(f"Error getting data from cache: {e}")
            return None
