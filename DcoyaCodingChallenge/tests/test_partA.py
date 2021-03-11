from partA import JWT_SECRET, JWT_ALGORITHM
import jwt
from time import time
import requests


class Saved:
    def __init__(self):
        self.bob_token = ''
        self.jim_token = ''


save = Saved()
TEST_STAMP = int(time())
LOCATION_A = 'http://127.0.0.1'


def test_register():
    rv = requests.post(LOCATION_A + '/register', json={'username': f'bob{TEST_STAMP}', 'password': "psw123"})
    token = rv.json()['token']
    token_data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
    assert token_data['username'] == f'bob{TEST_STAMP}'
    assert token_data['password'] == 'psw123'
    save.bob_token = token


def test_reg_inuse():
    rv = requests.post(LOCATION_A + '/register', json={'username': f'bob{TEST_STAMP}', 'password': "psw123"})
    assert rv.text == 'already registered'


def test_show():
    rv = requests.get(LOCATION_A + '/show')
    data = rv.json()
    assert f'bob{TEST_STAMP}' in data
    rv = requests.post(LOCATION_A + '/register', json={'username': f'jim{TEST_STAMP}', 'password': "123psw"})
    save.jim_token = rv.json()['token']
    rv = requests.get(LOCATION_A + '/show')
    data = rv.json()
    assert (f'bob{TEST_STAMP}' and f'jim{TEST_STAMP}') in data


def test_authorize():
    rv = requests.post(LOCATION_A + '/authorize', json={'token': save.bob_token})
    assert rv.text == 'valid'
    rv = requests.post(LOCATION_A + '/authorize', json={'token': 'hello'})
    assert rv.text == 'not a token'
    rv = requests.post(LOCATION_A + '/authorize', json={'token': save.jim_token})
    assert rv.text == 'valid'


def test_authorize_exp():
    payload = {'username': f'bob{TEST_STAMP}',
               'password': 'psw123',
               'exp': int(time() - 100),
               }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    rv = requests.post(LOCATION_A + '/authorize', json={'token': token})
    assert rv.text == 'expired token'


def test_removed_user():
    rv = requests.get(LOCATION_A + '/show')
    data = rv.json()
    assert f'bob{TEST_STAMP}' not in data


def test_cleanup():
    payload = {'username': f'jim{TEST_STAMP}',
               'password': '123psw',
               'exp': int(time() - 100),
               }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    requests.post(LOCATION_A + '/authorize', json={'token': token})
    rv = requests.get(LOCATION_A + '/show')
    data = rv.json()
    assert f'jim{TEST_STAMP}' not in data
