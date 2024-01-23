#!/usr/bin/env python3
"""module for task 10"""


def update_topics(mongo_collection, name, topics):
    """updates a document based on name"""
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
