#!/usr/bin/env python3
"""module for task 11"""


def schools_by_topic(mongo_collection, topic):
    """school by topic"""
    res = mongo_collection.find({"topics": topic})
    return res
