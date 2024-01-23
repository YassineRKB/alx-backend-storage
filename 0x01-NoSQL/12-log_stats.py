#!/usr/bin/env python3
"""module for task 12"""
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


if __name__ == "__main__":
    log()
