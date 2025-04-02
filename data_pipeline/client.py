"""
RestCountriesAPIClient class that is responsible for fetching data from the external API.
"""

from typing import List

import requests


class RestCountriesAPIClient:
    """
    Handles interaction with the external API.
    """

    API = "https://restcountries.com/v3.1/all"

    @staticmethod
    def fetch_countries() -> List[dict]:
        """
        Fetch the data from the API.

        Returns:
            List[dict]: A list of countries data.

        Raises:
            Exception: If the API request fails.
        """
        response = requests.get(RestCountriesAPIClient.API, timeout=10)

        match response.status_code:
            case 200:
                return response.json()
            case _:
                raise Exception(f"Couldn't fetch data from the API: {response.text}")
