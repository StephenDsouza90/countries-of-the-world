"""
This module contains the tests for the Processor class.
"""

import pytest
from unittest.mock import MagicMock

from data_pipeline.processor import Processor
from backend.db.manager import DatabaseManager
from cache.cache import CacheManager


def test_process_success():
    """
    Test the process method when the data is processed successfully.
    """
    countries = [
        {
            "name": {"common": "Country1"},
            "region": "Region1",
            "population": 1000,
            "area": 10,
        },
        {
            "name": {"common": "Country2"},
            "region": "Region2",
            "population": 2000,
            "area": 20,
        },
    ]

    db_manager = MagicMock(spec=DatabaseManager)
    mock_cache_manager = MagicMock(spec=CacheManager)
    db_manager.get_country.side_effect = [
        None,
        MagicMock(
            name="Country2",
            region="Region2",
            population=1000,
            area=10,
            population_density=100,
        ),
    ]
    mock_cache_manager.get_data.side_effect = [
        None,
        '{"name": "Country2", "region": "Region2", "population": 1000, "area": 10}',
    ]
    mock_cache_manager.set_data.return_value = True

    new_countries, updated_countries = Processor.process(
        countries, db_manager, mock_cache_manager
    )

    assert len(new_countries) == 1
    assert new_countries[0]["name"] == "Country1"
    assert new_countries[0]["population_density"] == 100
    assert new_countries[0]["area"] == 10
    assert new_countries[0]["region"] == "Region1"
    assert new_countries[0]["population"] == 1000

    assert len(updated_countries) == 1
    assert updated_countries[0]["name"] == "Country2"
    assert updated_countries[0]["population_density"] == 100
    assert updated_countries[0]["area"] == 20
    assert updated_countries[0]["population"] == 2000


def test_process_failure_with_key_error():
    """
    Test the process method when a KeyError is raised.
    """
    countries = [
        {
            "name": {"common": "Country1"},
            "region": "Region1",
            "population": 1000,
            "area": 10,
        },
        {
            "name": {"common": "Country2"},
            "region": "Region2",
            "population": 2000,
        },
    ]

    db_manager = MagicMock(spec=DatabaseManager)
    mock_cache_manager = MagicMock(spec=CacheManager)
    mock_cache_manager.get_data.return_value = '{"key": "value"}'

    with pytest.raises(KeyError):
        Processor.process(countries, db_manager, mock_cache_manager)
