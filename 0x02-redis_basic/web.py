#!/usr/bin/env python3

import requests
import redis
from typing import Callable

""" Initialize the Redis client"""
cache_client = redis.Redis()

def get_page(url: str) -> str:
    """ Define the cache key for HTML content and access count"""
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"
    
    """Check if the content is already in cache"""
    cached_content = cache_client.get(cache_key)
    if cached_content:
        """Return the cached content if available"""
        return cached_content.decode('utf-8')
    
    """If content is not cached, fetch it"""
    response = requests.get(url)
    content = response.text
    
    """Store the content in cache with a 10-second expiration"""
    cache_client.setex(cache_key, 10, content)
    
    """Increment the access count for the URL"""
    cache_client.incr(count_key)
    
    return content

def cache_with_count(expiration: int = 10):
    def decorator(func: Callable[[str], str]):
        def wrapper(url: str) -> str:
            """ Define cache and count keys"""
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            """ Check if the content is already cached"""
            cached_content = cache_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')

            """ Fetch the content if not cached"""
            content = func(url)

            """ Cache the result and set expiration"""
            cache_client.setex(cache_key, expiration, content)

            """ Increment the access count"""
            cache_client.incr(count_key)

            return content
        return wrapper
    return decorator

@cache_with_count(expiration=10)
def get_page(url: str) -> str:
    """ Fetch HTML content from the URL"""
    response = requests.get(url)
    return response.text
