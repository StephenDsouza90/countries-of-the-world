"""
This module contains the tests for the Handler class.
"""

import pytest
from unittest.mock import MagicMock

from data_pipeline.handler import Handler


@pytest.fixture
def mock_db_manager():
    """
    Fixture to mock the DatabaseManager.
    """
    return MagicMock()


def test_add_and_update_countries(mock_db_manager):
    """
    Test the add_and_update_countries method.
    """
    new_countries = [
        {
            "name": "Country1",
            "region": "Region1",
            "population": 1000,
            "area": 10,
        },
        {
            "name": "Country2",
            "region": "Region2",
            "population": 2000,
            "area": 20,
        },
    ]

    updated_countries = [
        {
            "name": "Country3",
            "region": "Region3",
            "population": 1000,
            "area": 10,
            "population_density": 100,
        }
    ]

    Handler.add_and_update_countries_to_database(
        mock_db_manager, new_countries, updated_countries
    )
    mock_db_manager.add_bulk_countries.assert_called_once_with(new_countries)
    mock_db_manager.update_bulk_countries.assert_called_once_with(updated_countries)
