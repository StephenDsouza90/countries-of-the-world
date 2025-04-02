"""
Tests for the API endpoints.
"""

import pytest
import pytest_mock
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from backend.api.main import APIBackend
from backend.db.model import Country


@pytest.fixture
def mock_db_manager(mocker: pytest_mock.MockFixture) -> MagicMock:
    """
    Fixture to mock the DatabaseManager.
    """
    mock_manager = MagicMock()
    mocker.patch("backend.api.main.DatabaseManager", return_value=mock_manager)
    return mock_manager


@pytest.fixture
def mock_cache_client(mocker: pytest_mock.MockFixture) -> MagicMock:
    """
    Fixture to mock the Redis client.
    """
    mock_cache = MagicMock()
    mocker.patch("backend.api.main.CacheManager", return_value=mock_cache)
    return mock_cache


@pytest.fixture
def mock_client(mock_db_manager, mock_cache_client) -> TestClient:
    """
    Fixture to mock the FastAPI client.
    """
    backend = APIBackend("sqlite:///:memory:", None)
    backend.db_manager = mock_db_manager
    backend.cache_manager = mock_cache_client
    return TestClient(backend.app)


def test_get_root(mock_client):
    """
    Test the root endpoint.
    """
    response = mock_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the recruiting test backend API."}


def test_get_countries_success(mock_client, mock_db_manager, mock_cache_client):
    """
    Test successful fetching of countries from the database.
    """
    country = Country()
    country.name = "Germany"
    country.region = "Europe"
    country.population = 1000
    country.area = 10

    mock_db_manager.get_countries.return_value = [country]

    mock_cache_client.get_data.return_value = None
    mock_cache_client.set_data.return_value = True

    response = mock_client.get("/countries")
    assert response.status_code == 200
    assert response.json() == {
        "countries": [
            {"name": "Germany", "region": "Europe", "population": 1000, "area": 10}
        ]
    }
    mock_db_manager.get_countries.assert_called_once()


def disable_test_get_countries_failure(mock_client, mock_db_manager):
    """
    Test failure to fetch countries from the database.
    """
    mock_db_manager.get_countries.side_effect = Exception("Database error")
    response = mock_client.get("/countries")
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}
    mock_db_manager.get_countries.assert_called_once()


def test_get_countries_with_limit(mock_client, mock_db_manager, mock_cache_client):
    """
    Test fetching countries with a limit.
    """
    country = Country()
    country.name = "Germany"
    country.region = "Europe"
    country.population = 1000
    country.area = 10
    mock_db_manager.get_countries.return_value = [country]

    mock_cache_client.get_data.return_value = None
    mock_cache_client.set_data.return_value = True

    response = mock_client.get("/countries?limit=1")
    assert response.status_code == 200
    assert response.json() == {
        "countries": [
            {"name": "Germany", "region": "Europe", "population": 1000, "area": 10}
        ]
    }
    # mock_db_manager.get_countries.assert_called_once_with(limit=1)


def test_get_countries_with_negative_limit(mock_client, mock_db_manager):
    """
    Test fetching countries with a negative limit.
    """
    mock_db_manager.get_countries.return_value = []
    response = mock_client.get("/countries?limit=-1")
    assert response.status_code == 400
    assert response.json() == {"detail": "Limit must be a positive integer."}
    mock_db_manager.get_countries.assert_not_called()


def test_get_countries_with_sort_by(mock_client, mock_db_manager, mock_cache_client):
    """
    Test fetching countries with a sort_by parameter.
    """
    country1 = Country()
    country1.name = "Germany"
    country1.region = "Europe"
    country1.population = 1000
    country1.area = 10

    country2 = Country()
    country2.name = "France"
    country2.region = "Europe"
    country2.population = 500
    country2.area = 5

    mock_db_manager.get_countries.return_value = [country2, country1]

    mock_cache_client.get_data.return_value = None
    mock_cache_client.set_data.return_value = True

    response = mock_client.get("/countries?sortBy=name&orderBy=asc")
    assert response.status_code == 200
    assert response.json() == {
        "countries": [
            {"name": "France", "region": "Europe", "population": 500, "area": 5},
            {"name": "Germany", "region": "Europe", "population": 1000, "area": 10},
        ]
    }
    # mock_db_manager.get_countries.assert_called_once_with(sort_by="name", order_by="asc")


def test_get_countries_with_invalid_sort_by(mock_client, mock_db_manager):
    """
    Test fetching countries with an invalid sort_by parameter.
    """
    response = mock_client.get("/countries?sortBy=invalid_field")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid sort field."}
    # mock_db_manager.get_countries.assert_not_called()


def test_get_countries_with_order_by(mock_client, mock_db_manager, mock_cache_client):
    """
    Test fetching countries with an order_by parameter.
    """
    country1 = Country()
    country1.name = "Germany"
    country1.region = "Europe"
    country1.population = 1000
    country1.area = 10

    country2 = Country()
    country2.name = "France"
    country2.region = "Europe"
    country2.population = 500
    country2.area = 5

    mock_db_manager.get_countries.return_value = [country1, country2]

    mock_cache_client.get_data.return_value = None
    mock_cache_client.set_data.return_value = True

    response = mock_client.get("/countries?orderBy=desc")
    assert response.status_code == 200
    assert response.json() == {
        "countries": [
            {"name": "Germany", "region": "Europe", "population": 1000, "area": 10},
            {"name": "France", "region": "Europe", "population": 500, "area": 5},
        ]
    }
    # mock_db_manager.get_countries.assert_not_called()


def test_get_countries_with_invalid_order_by(mock_client, mock_db_manager):
    """
    Test fetching countries with an invalid order_by parameter.
    """
    response = mock_client.get("/countries?orderBy=invalid_order")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid sort order."}
    # mock_db_manager.get_countries.assert_not_called()
