import os
from pymongo import MongoClient
from typing import List, Optional


# connect to mongodb
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
    """Connects to urparts collection to retrieve
    its records considering query strings.

    Args:
        manufacturer (str, optional): A manufacturer query. Defaults to None.
        category (str, optional): A category query. Defaults to None.
        model (str, optional): A model query. Defaults to None.
        part (str, optional): A part query. Defaults to None.
        part_category (str, optional): A part categoruy query. Defaults to None.

    Returns:
        List: A filtered list of records.
    """
    query = {}
    if manufacturer:
        query.setdefault(
            "manufacturer",
            manufacturer
            # {"$regex": ".*{value}.*".format(value=manufacturer)}
        )
    if category:
        query.setdefault(
            "category",
            category
            # {"$regex": ".*{value}.*".format(value=category)}
        )
    if model:
        query.setdefault(
            "model",
            model
            # {"$regex": ".*{value}.*".format(value=model)}
        )
    if part:
        query.setdefault(
            "part",
            part
            # {"$regex": ".*{value}.*".format(value=part)}
        )
    if part_category:
        query.setdefault(
            "part_category",
            part_category
            # {"$regex": ".*{value}.*".format(value=part_category)}
        )
    
    if len(query):
        return list(collection.find(query).limit(100))
    return list(collection.find().limit(100))
