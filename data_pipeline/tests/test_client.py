"""
This module contains tests for the data_pipeline.client module.
"""

import pytest
from unittest.mock import patch, Mock

from data_pipeline.client import RestCountriesAPIClient


def test_fetch_countries_success():
    """
    Test the fetch_countries method when the API returns a 200 status code.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "name": {"common": "Country1"},
            "region": "Region1",
            "population": 1000,
            "area": 10,
        }
    ]

    with patch("data_pipeline.client.requests.get", return_value=mock_response):
        result = RestCountriesAPIClient.fetch_countries()
        assert result == [
            {
                "name": {"common": "Country1"},
                "region": "Region1",
                "population": 1000,
                "area": 10,
            }
        ]


def test_fetch_countries_failure():
    """
    Test the fetch_countries method when the API returns a non-200 status code.
    """
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("data_pipeline.client.requests.get", return_value=mock_response):
        with pytest.raises(
            Exception, match="Couldn't fetch data from the API: Internal Server Error"
        ):
            RestCountriesAPIClient.fetch_countries()
