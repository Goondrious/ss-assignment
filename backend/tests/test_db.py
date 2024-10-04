import pytest
from datetime import datetime

from utils.db import get_db, get_user, get_user_image, get_user_image_count, get_user_images, init_db, set_db, updateUser
from utils.types import DATE_FORMAT, User, UserImage

def test_init_db():
    init_db(True)

    dbJSON = get_db()
    assert type(dbJSON) == dict
    assert type(dbJSON["users"]) == dict

def test_get_db():
    dbJSON = get_db()
    assert type(dbJSON) == dict

def test_set_db():
    testKey = "test"
    testValue = "value"

    def test_update(dbJSON):
        dbJSON[testKey] = testValue
        return dbJSON

    set_db(test_update)
    dbJSON = get_db()
    assert type(dbJSON) == dict
    assert dbJSON[testKey] == testValue

def test_get_user():
    username = "test-user"
    id = '123'
    user = User(username=username, id=id, password="")

    def test_update(dbJSON):
        dbJSON["users"][username] = vars(user)
        return dbJSON

    set_db(test_update)
    user = get_user(username)
    assert user is not None
    assert user.id == id

def test_get_user_images():
    user_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["images"][user_id] = test_value
        return dbJSON

    set_db(test_update)
    db_value = get_user_images(user_id)
    assert db_value is not None
    assert db_value["a"] == 1

def test_get_user_image_count():
    user_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["images"][user_id] = test_value
        return dbJSON

    set_db(test_update)
    count = get_user_image_count(user_id)
    assert count == 2

def test_get_user_image():
    user_id = "123"
    image_id = "456"
    date_string = datetime.now().strftime(DATE_FORMAT)
    image_json = { "num_compressions": 1, "user_id": user_id, "id": image_id, "name": "test", "path": "/a/b/c",  "extension": ".jpg", "size": 100, "uploaded_at": date_string  }
    test_image = UserImage(**image_json)

    def test_update(dbJSON):
        dbJSON["images"][user_id][image_id] = image_json
        return dbJSON

    set_db(test_update)
    db_image = get_user_image(user_id, image_id)
    assert db_image is not None
    assert test_image == db_image
    assert test_image.id == db_image.id
    assert test_image.name == db_image.name
    assert test_image.path == db_image.path



