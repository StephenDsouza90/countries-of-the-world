"""
Redis client for connecting to a Redis server.
This module provides a simple interface to connect to a Redis server using the redis-py library.
It includes a connection to a Redis server running on localhost at port 6379.
"""

import redis

redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
