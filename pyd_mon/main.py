from bson.errors import InvalidId
from pydantic import BaseModel
from bson.objectid import ObjectId


class MongoId(ObjectId):
    """ObjectId Wrapper that adds validation functions for Pydantic"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not cls.is_valid(str(v)):
            raise InvalidId("Invalid ObjectId")

        return cls(str(v))


class MongoModel(BaseModel):
    """Extended Pydantic BaseModel to map MongoDb's `_id` to an `id` field."""

    @classmethod
    def from_mongo(cls, data: dict):
        """Create a Pydantic model instance mapping `_id` to `id`."""
        if not data:
            return data
        id = data.pop("_id", None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        """Create a dict of the current instance mapping `id` to `_id`."""
        parsed = self.dict(**kwargs)
        parsed["_id"] = parsed.pop("id")
        return parsed

    class Config:
        json_encoders = {MongoId: lambda id: str(id)}
