# Pyd_Mon

An easy way to convert and validate Pymongo ObjectId's with Pydantic model fields.

# Usage

## Creating a MongoModel

Creating Pydantic models with a mapping id is as easy as inheriting from MongoModel and creating an `id` field with type of `MongoId`. All of your other fields can be created as normal pydantic fields.

```python
from pyd_mon import MongoModel, MongoId

class Item(MongoModel):
    id: MongoId # Will map to '_id'
    name: str # The rest of the fields are standard Pydantic fields
```

## Create Pydantic instance from Pymongo dict (`_id` -> `id`)

To map from a Pymongo dict you can use the `from_mongo` class method on your model.

```python
result = collection.find_one() # Get item from Pymongo
item = Item.from_mongo(result) # Create a Pydantic instance from the Pymongo dict.
```

## Create Pymongo dict from Pydantic instance (`id` -> `_id`)

To map back from a pydantic instance to a Pymongo dict call the `mongo` method on your model instance.

```python
item = Item(id=MongoId(), name='Example')
collection.insert_one(item.mongo())
```
