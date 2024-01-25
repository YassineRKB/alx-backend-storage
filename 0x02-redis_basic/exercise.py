#!/usr/bin/env python3
"""Module forexpiring web cache and tracker"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a function has been called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function"""
        self._redis.incr(method.__qualname__) if isinstance(self._redis, redis.Redis) else None
        return method(self, *args, **kwargs)

    return wrapper

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

    def get(self, key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """method that gets cache data"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Method to get a string from Redis"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Method to get an int from Redis"""
        return self.get(key, lambda x: int(x))
