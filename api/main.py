import uvicorn
import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from schemas import Part
from typing import List, Optional
import random


tags_metadata = [
    {
        "name": "parts",
        "description": "List machinery parts.",
    }
]

app = FastAPI(
    title="UrParts API",
    description="API for consulting machinery parts and its information.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

client = MongoClient(os.environ['MONGO_URL'])
base = client.urparts
collection = base.urparts


@app.get("/parts", response_model=List[Part], tags=["parts"])
async def view_urparts(
    manufacturer: Optional[str] = None,
    category: Optional[str] = None,
    model: Optional[str] = None,
    part: Optional[str] = None,
    part_category: Optional[str] = None
):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
