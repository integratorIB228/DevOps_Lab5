from fastapi.testclient import TestClient
from src.main import app

_c = TestClient(app)

_u = [
    {"id": 1, "name": "Ivan Ivanov",  "email": "i.i.ivanov@mail.com"},
    {"id": 2, "name": "Petr Petrov",  "email": "p.p.petrov@mail.com"},
]

_ep  = "/api/v1/user"
_e0  = _u[0]["email"]
_nil = "no@mail.com"
_tmp = "test@mail.com"


def test_get_existed_user():
    '''Получение существующего пользователя'''
    _r = _c.get(_ep, params={"email": _e0})
    assert _r.status_code == 200
    assert _r.json() == _u[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    _r = _c.get(_ep, params={"email": _nil})
    assert _r.status_code == 404
    assert _r.json() == {"detail": "User not found"}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    _r = _c.post(_ep, json={"name": "Test", "email": _tmp})
    assert _r.status_code == 201
    assert isinstance(_r.json(), int)


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    _r = _c.post(_ep, json={"name": "Test", "email": _e0})
    assert _r.status_code == 409


def test_delete_user():
    '''Удаление пользователя'''
    _r = _c.delete(_ep, params={"email": _tmp})
    assert _r.status_code == 204