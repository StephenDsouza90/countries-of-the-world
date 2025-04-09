from unittest.mock import patch, MagicMock
from internal.cache.client import RedisClient


@patch("internal.cache.client.redis.StrictRedis")
def test_redis_client_initialization(mock_strict_redis):
    # Arrange
    mock_redis_instance = MagicMock()
    mock_strict_redis.return_value = mock_redis_instance

    # Act
    client = RedisClient(host="test_host", port=1234, decode_responses=False)

    # Assert
    mock_strict_redis.assert_called_once_with(
        host="test_host", port=1234, decode_responses=False
    )
    assert client.redis_client == mock_redis_instance


@patch("internal.cache.client.redis.StrictRedis")
def test_get_client(mock_strict_redis):
    # Arrange
    mock_redis_instance = MagicMock()
    mock_strict_redis.return_value = mock_redis_instance
    client = RedisClient()

    # Act
    redis_client = client.get_client()

    # Assert
    assert redis_client == mock_redis_instance
