from unittest.mock import MagicMock
from internal.cache.cache import CacheManager


def test_set_data_success():
    # Arrange
    mock_client = MagicMock()
    mock_client.set.return_value = True
    cache_manager = CacheManager(client=mock_client)

    # Act
    result = cache_manager.set_data("test_key", "test_value")

    # Assert
    mock_client.set.assert_called_once_with("test_key", "test_value", ex=60 * 60 * 24)
    assert result is True


def test_set_data_failure():
    # Arrange
    mock_client = MagicMock()
    mock_client.set.side_effect = Exception("Redis error")
    cache_manager = CacheManager(client=mock_client)

    # Act
    result = cache_manager.set_data("test_key", "test_value")

    # Assert
    mock_client.set.assert_called_once_with("test_key", "test_value", ex=60 * 60 * 24)
    assert result is False


def test_get_data_success():
    # Arrange
    mock_client = MagicMock()
    mock_client.get.return_value = "test_value"
    cache_manager = CacheManager(client=mock_client)

    # Act
    result = cache_manager.get_data("test_key")

    # Assert
    mock_client.get.assert_called_once_with("test_key")
    assert result == "test_value"


def test_get_data_failure():
    # Arrange
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Redis error")
    cache_manager = CacheManager(client=mock_client)

    # Act
    result = cache_manager.get_data("test_key")

    # Assert
    mock_client.get.assert_called_once_with("test_key")
    assert result is None
