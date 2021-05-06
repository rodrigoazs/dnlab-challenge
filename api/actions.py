import os
from pymongo import MongoClient
from typing import List, Optional
import random


client = MongoClient(os.environ['MONGO_URL'])
base = client.urparts
collection = base.urparts


def action_view_urparts(
    manufacturer: Optional[str] = None,
    category: Optional[str] = None,
    model: Optional[str] = None,
    part: Optional[str] = None,
    part_category: Optional[str] = None
):
    collection.insert_many([
        {
            "manufacturer": "Ammann",
            "category": "Roller Parts",
            "model": "ASC10{}".format(random.randint(3, 9)),
            "part": "ND011710",
            "part_category": "LEFT COVER"
        }
    ])

    query = {}
    if manufacturer:
        query.setdefault(
            "manufacter",
            {"$regex": ".*{value}.*".format(value=manufacturer)}
        )
    if category:
        query.setdefault(
            "category",
            {"$regex": ".*{value}.*".format(value=category)}
        )
    if model:
        query.setdefault(
            "model",
            {"$regex": ".*{value}.*".format(value=model)}
        )
    if part:
        query.setdefault(
            "part",
            {"$regex": ".*{value}.*".format(value=part)}
        )
    if part_category:
        query.setdefault(
            "part_category",
            {"$regex": ".*{value}.*".format(value=part_category)}
        )
    
    if len(query):
        return list(collection.find(query))
    return list(collection.find())
