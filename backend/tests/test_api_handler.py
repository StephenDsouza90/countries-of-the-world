import pytest
from unittest.mock import MagicMock
from internal.db.manager import NoSQLDatabaseManager
from internal.cache.cache import CacheManager
from backend.handler import RequestHandler


@pytest.fixture
def mock_db_manager():
    return MagicMock(spec=NoSQLDatabaseManager)


@pytest.fixture
def mock_cache_manager():
    return MagicMock(spec=CacheManager)


@pytest.fixture
def request_handler(mock_db_manager, mock_cache_manager):
    return RequestHandler(mock_db_manager, mock_cache_manager)


def test_get_countries_from_cache(request_handler, mock_cache_manager):
    mock_cache_manager.get_data.return_value = '[{"country_name": "CountryA"}]'
    result = request_handler.get_countries(10, "population", "asc")
    assert result == [{"country_name": "CountryA"}]
    mock_cache_manager.get_data.assert_called_once_with(
        "countries:limit=10:sort_by=population:order_by=asc"
    )


def test_get_countries_from_db(request_handler, mock_db_manager, mock_cache_manager):
    mock_cache_manager.get_data.return_value = None
    mock_db_manager.get_countries.return_value = [
        {
            "country_name": "CountryA",
            "population_density": 100,
            "area": 500,
            "population": 50000,
            "region": "RegionA",
        }
    ]
    result = request_handler.get_countries(10, "population", "asc")
    assert result == [
        {
            "country_name": "CountryA",
            "population_density": 100,
            "area": 500,
            "population": 50000,
            "region": "RegionA",
        }
    ]
    mock_db_manager.get_countries.assert_called_once_with(10, "population", "asc")
    mock_cache_manager.set_data.assert_called_once()


def test_get_country_from_cache(request_handler, mock_cache_manager):
    mock_cache_manager.get_dict_data.return_value = {"country_name": "CountryA"}
    result = request_handler.get_country("CountryA")
    assert result == {"country_name": "CountryA"}
    mock_cache_manager.get_dict_data.assert_called_once_with("country:CountryA")


def test_get_country_from_db(request_handler, mock_db_manager, mock_cache_manager):
    mock_cache_manager.get_dict_data.return_value = None
    mock_db_manager.get_country.return_value = {
        "country_name": "CountryA",
        "population_density": 100,
        "area": 500,
        "population": 50000,
        "region": "RegionA",
    }
    result = request_handler.get_country("CountryA")
    assert result == {
        "country_name": "CountryA",
        "population_density": 100,
        "area": 500,
        "population": 50000,
        "region": "RegionA",
    }
    mock_db_manager.get_country.assert_called_once_with("CountryA")
    mock_cache_manager.set_dict_data.assert_called_once()


def test_upload_image(request_handler, mock_db_manager, mock_cache_manager, tmp_path):
    mock_cache_manager.get_data.return_value = None
    mock_db_manager.add_image.return_value = None

    # Use a temporary directory for file operations
    temp_dir = tmp_path / "assets/CountryA/images"
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / "test_image.jpg"

    file_content = b"test_image_data"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Mock the _get_file_path method to return the temporary file path
    request_handler._get_file_path = MagicMock(return_value=str(file_path))

    image_id = request_handler.upload_image(
        "CountryA", file_content, "Test Title", "Test Description"
    )
    assert len(image_id) == 32  # Random hex ID of 16 bytes
    mock_db_manager.add_image.assert_called_once()
    mock_cache_manager.set_data.assert_called_once()


def test_get_images_from_cache(request_handler, mock_cache_manager):
    mock_cache_manager.get_data.return_value = '[{"image_id": "img123"}]'
    result = request_handler.get_images("CountryA")
    assert result == [{"image_id": "img123"}]
    mock_cache_manager.get_data.assert_called_once_with("images:CountryA")


def test_get_images_from_db(
    request_handler, mock_db_manager, mock_cache_manager, tmp_path
):
    mock_cache_manager.get_data.return_value = None
    mock_db_manager.get_images.return_value = [
        {"image_id": "img123", "title": "Test", "description": "Test Desc"}
    ]

    # Create the expected file path
    image_path = tmp_path / "assets/CountryA/images/img123.jpg"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"test_image_data")

    # Mock the _get_file_path method to return the correct file path
    request_handler._get_file_path = MagicMock(return_value=str(image_path))

    result = request_handler.get_images("CountryA")
    assert len(result) == 1
    assert result[0]["image_id"] == "img123"
    assert result[0]["file"] == "dGVzdF9pbWFnZV9kYXRh"  # Base64 encoded content
    mock_cache_manager.set_data.assert_called_once()
