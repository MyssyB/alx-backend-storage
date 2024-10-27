#!/usr/bin/env python3
"""inserts a new document"""

def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection with kwargs params:
    mongo_collection: objects of the mongo collection
    kwargs: key value pair of the data to add to the db"""
    d_insert = {}
    for key,value in kwargs.items():
        d_insert[key] = value
    if len(d_insert) > 0:
        adder = mongo_collection.insert_one(d_insert)
        return adder.inserted_id
