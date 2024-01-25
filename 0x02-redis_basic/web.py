#!/usr/bin/env python3
"""module for using redis for basic cache"""
import redis
import requests
from typing import Callable
from functools import wraps


store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """Decorator that caches the output of a function using Redis."""
    @wraps(method)
    def invoker(url) -> str:
        """Invoker function"""
        store.incr(f'count:{url}')
        result = store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        store.set(f'count:{url}', 0)
        store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it."""
    return requests.get(url).text
