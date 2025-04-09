"""
Redis client for connecting to a Redis server.
This module provides a simple interface to connect to a Redis server using the redis-py library.
It includes a connection to a Redis server running on localhost at port 6379.
"""

import redis


class RedisClient:
    """
    A class to create a Redis client for connecting to a Redis server.
    It uses the redis-py library to establish the connection.
    """

    def __init__(self, host="redis", port=6379, decode_responses=True):
        self.redis_client = redis.StrictRedis(
            host=host, port=port, decode_responses=decode_responses
        )

    def get_client(self):
        return self.redis_client
