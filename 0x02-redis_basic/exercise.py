#!/usr/bin/env python3
"""Module forexpiring web cache and tracker"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class"""

    def __init__(self):
        """Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that stores cache data"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
