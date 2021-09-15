import json
import pytest
from bson.errors import InvalidId
from pyd_mon import __version__, MongoId, MongoModel

VALID_ID = "614128f7a86d0924243378d3"
INVALID_ID = "1234"


class Item(MongoModel):
    id: MongoId


def test_version():
    assert __version__ == "0.1.0"


def test_mongo_id_valid():
    Item(id=MongoId(VALID_ID))
    Item(id=VALID_ID)


def test_mongo_id_invalid():
    with pytest.raises(InvalidId):
        Item(id=MongoId(INVALID_ID))
    with pytest.raises(InvalidId):
        Item(id=INVALID_ID)


def test_mongo_model_from_mongo():
    mongo_data = {"_id": MongoId(VALID_ID)}
    expected = {"id": MongoId(VALID_ID)}
    assert Item.from_mongo(mongo_data).dict() == expected


def test_mongo_model_mongo():
    expected = {"_id": MongoId(VALID_ID)}
    assert Item(id=MongoId(VALID_ID)).mongo() == expected


def test_mongo_model_from_mongo_no_data():
    expected = None
    assert Item.from_mongo(None) == expected


def test_mongo_model_from_mongo_list():
    mongo_data = [{"_id": MongoId(VALID_ID)}, {"_id": MongoId(VALID_ID)}]
    expected = [Item(id=MongoId(VALID_ID)), Item(id=MongoId(VALID_ID))]
    assert Item.from_mongo_list(mongo_data) == expected


def test_mongo_model_schema():
    Item.schema()


def test_mongo_model_json():
    item = Item(id=VALID_ID)
    expected = json.dumps({"id": VALID_ID})
    assert item.json() == expected
