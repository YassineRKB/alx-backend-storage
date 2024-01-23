#!/usr/bin/env python3
"""module for task 9"""


def insert_school(mongo_collection, **kwargs):
    """inserting a document in a collection based on kwargs"""
    res = mongo_collection.insert_one(kwargs).inserted_id
    return res
