from datetime import datetime
from typing import List, Optional
from pymongo import MongoClient
from fastapi import FastAPI, Depends
from pyd_mon import MongoModel, MongoId

app = FastAPI()


def get_db():
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["test-database"]
        yield db


class ItemBase(MongoModel):
    name: str
    price: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: MongoId
    created_at: Optional[datetime]


@app.get("/items", response_model=List[Item])
def root(db=Depends(get_db)):
    col = db["items"]
    return Item.from_mongo_list(col.find())


@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, db=Depends(get_db)):
    col = db["items"]
    new_id = col.insert_one(
        {**item.dict(exclude_unset=True), "created_at": datetime.utcnow()}
    ).inserted_id
    return Item.from_mongo(col.find_one({"_id": new_id}))
