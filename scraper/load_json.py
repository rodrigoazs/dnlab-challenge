import time
import json
from pymongo import MongoClient


if __name__ == "__main__":
    start_time = time.time()

    with open('data.json') as json_file:
        data = json.load(json_file)

    client = MongoClient('mongodb://mongodb:mongodb@mongodb:27017/')
    base = client.urparts
    collection = base.urparts

    collection.insert_many(data)

    print("Inserted %s parts" % (len(data)))

    collection.create_index([
        ("manufacturer", "text"),
        ("category", "text"),
        ("model", "text"),
        ("part", "text"),
        ("part_category", "text"),
    ])

    print("Created indexes")

    print("--- Script took %s seconds ---" % (time.time() - start_time))
