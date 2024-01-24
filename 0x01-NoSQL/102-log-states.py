#!/usr/bin/env python3
"""module for task 15"""
from pymongo import MongoClient


def log():
    """loging stats from the database"""
    client = MongoClient('mongodb://localhost:27017')
    data = client.logs.nginx
    print(data.count_documents({}), "logs")
    print("Methods:")
    print("\tmethod GET:", data.count_documents({"method": "GET"}))
    print("\tmethod POST:", data.count_documents({"method": "POST"}))
    print("\tmethod PUT:", data.count_documents({"method": "PUT"}))
    print("\tmethod PATCH:", data.count_documents({"method": "PATCH"}))
    print("\tmethod DELETE:", data.count_documents({"method": "DELETE"}))
    print(data.count_documents({"method": "GET", "path": "/status"}),
          "status check")
    print('IPs:')
    pipes = [
            {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
    ]
    curated = list(data.aggregate(pipes))
    for ip in curated:
        print('\t{}: {}'.format(ip['_id'], ip['count']))


if __name__ == "__main__":
    log()
