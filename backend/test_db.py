import pytest

from backend.utils.db import get_db, init_db, set_db, updateUser

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

def test_update_user():
    testKey = "test"
    testValue = "value"

    updateUser(testKey, testValue)

    dbJSON = get_db()
    assert type(dbJSON) == dict
    assert dbJSON.users[testKey] == testValue
