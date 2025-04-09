from unittest.mock import MagicMock
import pytest
import json
from data_pipeline.handler import Handler


@pytest.fixture
def mock_db_manager():
    return MagicMock()


@pytest.fixture
def mock_cache_manager():
    return MagicMock()


@pytest.fixture
def handler(mock_db_manager, mock_cache_manager):
    return Handler(db_manager=mock_db_manager, cache_manager=mock_cache_manager)


def test_process_countries_add_new_country(
    handler, mock_db_manager, mock_cache_manager
):
    countries = [
        {
            "name": {"common": "CountryA"},
            "population": 1000000,
            "area": 50000,
        }
    ]

    mock_cache_manager.get_data.return_value = None
    mock_db_manager.get_country.return_value = None

    handler.process_countries(countries)

    mock_db_manager.add_country.assert_called_once_with(
        "CountryA",
        {
            "name": {"common": "CountryA"},
            "population": 1000000,
            "area": 50000,
            "country_name": "CountryA",
            "population_density": 20.0,
        },
    )
    mock_cache_manager.set_data.assert_called_once_with(
        "CountryA",
        json.dumps(
            {
                "name": {"common": "CountryA"},
                "population": 1000000,
                "area": 50000,
                "country_name": "CountryA",
                "population_density": 20.0,
            }
        ),
    )


def test_process_countries_update_existing_country(
    handler, mock_db_manager, mock_cache_manager
):
    countries = [
        {
            "name": {"common": "CountryB"},
            "population": 2000000,
            "area": 100000,
        }
    ]

    existing_data = {
        "name": {"common": "CountryB"},
        "population": 1500000,
        "area": 100000,
        "country_name": "CountryB",
        "population_density": 15.0,
    }

    mock_cache_manager.get_data.return_value = json.dumps(existing_data)

    handler.process_countries(countries)

    mock_db_manager.update_country.assert_called_once_with(
        "CountryB",
        {
            "name": {"common": "CountryB"},
            "population": 2000000,
            "area": 100000,
            "country_name": "CountryB",
            "population_density": 20.0,
        },
    )
    mock_cache_manager.set_data.assert_called_once_with(
        "CountryB",
        json.dumps(
            {
                "name": {"common": "CountryB"},
                "population": 2000000,
                "area": 100000,
                "country_name": "CountryB",
                "population_density": 20.0,
            }
        ),
    )


def test_process_countries_skip_unchanged_country(
    handler, mock_db_manager, mock_cache_manager
):
    countries = [
        {
            "name": {"common": "CountryC"},
            "population": 3000000,
            "area": 150000,
        }
    ]

    existing_data = {
        "name": {"common": "CountryC"},
        "population": 3000000,
        "area": 150000,
        "country_name": "CountryC",
        "population_density": 20.0,
    }

    mock_cache_manager.get_data.return_value = json.dumps(existing_data)

    handler.process_countries(countries)

    mock_db_manager.update_country.assert_not_called()
    mock_cache_manager.set_data.assert_not_called()


def test_process_countries_key_error(handler):
    countries = [
        {
            "name": {"common": "CountryD"},
            "population": 4000000,
            # Missing "area" key
        }
    ]

    with pytest.raises(KeyError, match="Couldn't process country: 'area'"):
        handler.process_countries(countries)
