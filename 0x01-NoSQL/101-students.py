#!/usr/bin/env python3
"""module for task 14"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    res = mongo_collection.aggregate(
        [
            {"$unwind": "$topics"},
            {
                "$group": {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "averageScore": {"$avg": "$topics.score"},
                }
            },
            {"$sort": {"averageScore": -1}},
        ]

    )
    return res
