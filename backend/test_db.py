import pytest
from pathlib import Path
from datetime import datetime

from utils.settings import current_settings
from utils.db import create_user_image_compression_db, create_user_image_db, delete_user_image_compression_db, delete_user_image_db, get_db, get_user_image_compression_db, get_user_image_compressions_db, get_user_db, get_user_image_compression_count_db, get_user_image_db, get_user_image_count_db, get_user_images_db, init_db, set_db
from utils.types import DATE_FORMAT, User, UserImage, UserImageCompression

test_db_path = f"{current_settings.base_path}/db-test.json"

@pytest.fixture(scope='function')
def db_resource(request):
    init_db(test_db_path, True)

    def db_teardown():
        file = Path(test_db_path)
        file.unlink()

    request.addfinalizer(db_teardown)

    dbJSON = get_db(test_db_path)

    return dbJSON

def test_init_db():
    init_db(test_db_path, True)
    dbJSON = get_db(test_db_path)

    assert type(dbJSON) == dict
    assert type(dbJSON["users"]) == dict
    assert type(dbJSON["images"]) == dict
    assert type(dbJSON["compressions"]) == dict

    file = Path(test_db_path)
    file.unlink()

def test_get_db(db_resource):
    assert type(db_resource) == dict

def test_set_db(db_resource):
    testKey = "test"
    testValue = "value"

    def test_update(dbJSON):
        dbJSON[testKey] = testValue
        return dbJSON

    set_db(test_db_path, test_update)

    dbJSON = get_db(test_db_path)
    assert type(dbJSON) == dict
    assert dbJSON[testKey] == testValue

def test_get_user(db_resource):
    username = "test-user"
    id = '123'
    user = User(username=username, id=id, password="")

    def test_update(dbJSON):
        dbJSON["users"][username] = vars(user)
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    user = get_user_db(dbJSON, username)
    assert user is not None
    assert user.id == id

def test_get_user_images(db_resource):
    user_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["images"][user_id] = test_value
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    db_value = get_user_images_db(dbJSON, user_id)
    assert db_value is not None
    assert db_value["a"] == 1

def test_get_user_image_count(db_resource):
    user_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["images"][user_id] = test_value
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    count = get_user_image_count_db(dbJSON, user_id)
    assert count == 2

def test_get_user_image(db_resource):
    user_id = "123"
    image_id = "456"
    date_string = datetime.now().strftime(DATE_FORMAT)
    user_json = {}
    image_json = { "num_compressions": 1, "user_id": user_id, "id": image_id, "name": "test", "path": "/a/b/c",  "extension": ".jpg", "size": 100, "uploaded_at": date_string  }
    user_json[image_id] = image_json
    test_image = UserImage(**image_json)

    def test_update(dbJSON):
        dbJSON["images"][user_id] = user_json
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)
    db_image = get_user_image_db(dbJSON, user_id, image_id)
    assert db_image is not None
    assert test_image == db_image
    assert test_image.id == db_image.id
    assert test_image.name == db_image.name
    assert test_image.path == db_image.path

def test_get_user_image_compressions(db_resource):
    image_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["compressions"][image_id] = test_value
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    db_value = get_user_image_compressions_db(dbJSON, image_id)
    assert db_value is not None
    assert db_value["a"] == 1

def test_get_user_image_compression_count(db_resource):
    image_id = '123'
    test_value = { "a": 1, "b": 2 }

    def test_update(dbJSON):
        dbJSON["compressions"][image_id] = test_value
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    count = get_user_image_compression_count_db(dbJSON, image_id)
    assert count == 2

def test_get_user_image_compression(db_resource):
    image_id = '123'
    compression_id = '456'
    compression = UserImageCompression(
       id = compression_id,
        image_id= image_id,
        path = "/",
        quality = 10,
        created_at = "123",
    )
    update = {}
    update[compression_id] = vars(compression)

    def test_update(dbJSON):
        dbJSON["compressions"][image_id] = update
        return dbJSON

    set_db(test_db_path, test_update)
    dbJSON = get_db(test_db_path)

    db_value = get_user_image_compression_db(dbJSON, image_id, compression_id)
    assert db_value is not None
    assert db_value.id == compression_id
    assert db_value.image_id == image_id

def test_create_user_image(db_resource):
    user_id = 'abc'
    image_id = '123'
    image = UserImage(
        user_id = user_id,
        id = image_id,
        path = "/",
        name = "test image",
        extension = 'png',
        size = 10,
        uploaded_at = "123",
    )


    create_user_image_db(test_db_path, user_id, image)
    dbJSON = get_db(test_db_path)
    db_image = get_user_image_db(dbJSON, user_id, image_id)

    assert db_image is not None
    assert db_image.id == image_id
    assert db_image.user_id == user_id

def test_delete_user_image(db_resource):
    user_id = 'abc'
    image_id = '123'
    image = UserImage(
        user_id = user_id,
        id = image_id,
        path = "/",
        name = "test image",
        extension = 'png',
        size = 10,
        uploaded_at = "123",
    )

    create_user_image_db(test_db_path, user_id, image)
    delete_user_image_db(test_db_path, user_id, image_id)
    dbJSON = get_db(test_db_path)

    db_image = get_user_image_db(dbJSON, user_id, image_id)
    assert db_image is None

def test_create_user_image_compression(db_resource):
    compression_id = 'abc'
    image_id = '123'
    compression = UserImageCompression(
        id = compression_id,
        image_id= image_id,
        path = "/",
        quality = 10,
        created_at = "123",
    )

    create_user_image_compression_db(test_db_path, compression)
    dbJSON = get_db(test_db_path)
    db_compression = get_user_image_compression_db(dbJSON, image_id, compression_id)

    assert db_compression is not None
    assert db_compression.id == compression_id
    assert db_compression.image_id == image_id

def test_delete_user_image_compression(db_resource):
    compression_id = 'abc'
    image_id = '123'
    compression = UserImageCompression(
        id = compression_id,
        image_id= image_id,
        path = "/",
        quality = 10,
        created_at = "123",
    )

    create_user_image_compression_db(test_db_path, compression)
    delete_user_image_compression_db(test_db_path, image_id, compression_id)

    dbJSON = get_db(test_db_path)
    db_compression = get_user_image_compression_db(dbJSON, image_id, compression_id)

    assert db_compression is None
  