from crm import User
import pytest
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    u=User(first_name="Patrick",
           last_name="Martin",
           address="1 rue du chemin 75000 Paris",
           phone_number="0123456789")
    u.save()
    return u

def test_full_name(user):
    assert user.full_name =="Patrick Mfartin"


def test__check_phone_number():
    assert False


def test__check_names():
    assert False


def test_save():
    assert False
