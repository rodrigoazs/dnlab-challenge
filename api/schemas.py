from pydantic import BaseModel, Field
from pyobject import PyObjectId
from bson import ObjectId


class Part(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    manufacturer: str = Field(...)
    category: str = Field(...)
    model: str = Field(...)
    part: str = Field(...)
    part_category: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "manufacturer": "Ammann",
                "category": "Roller Parts",
                "model": "ASC100",
                "part": "ND011710",
                "part_category": "LEFT COVER"
            }
        }
