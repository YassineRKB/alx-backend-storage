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
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for function"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invoker function"""
        inkey = '{}:inputs'.format(method.__qualname__)
        outkey = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inkey, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outkey, output)
        return output
    return invoker


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    if not is_valid_method(method):
        return
    rep = get_redis_instance(method)
    if not rep:
        return
    name = method.__qualname__
    count = get_call_count(rep, name)
    if count == 0:
        return
    print(f'{name} was called {count} times:')
    print_call_history(rep, name)


def is_valid_method(method: Callable) -> bool:
    """Check if the method is valid for replay."""
    return method is not None and hasattr(method, '__self__')


def get_redis_instance(method: Callable) -> redis.Redis:
    """Get the Redis instance from the method's __self__ attribute."""
    return getattr(method.__self__, '_redis', None)


def get_call_count(rep: redis.Redis, name: str) -> int:
    """Get the call count from the Redis instance."""
    return int(rep.get(name)) if rep.exists(name) > 0 else 0


def print_call_history(rep: redis.Redis, name: str) -> None:
    """Print the call history of the method."""
    inputs = rep.lrange(f'{name}:inputs', 0, -1)
    outputs = rep.lrange(f'{name}:outputs', 0, -1)
    for i, o in zip(inputs, outputs):
        print(f'{name}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}')


class Cache:
    """Cache class"""

    def __init__(self):
        """Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
