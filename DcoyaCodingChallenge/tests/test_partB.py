import requests
from time import time, strftime
from partA import JWT_SECRET, JWT_ALGORITHM
import jwt


class Token:
    def __init__(self):
        self.token = ''


token = Token()
TEST_STAMP = int(time())
LOCATION_B = 'http://127.0.0.1:5000'
LOCATION_A = 'http://127.0.0.1'


def test_echo():
    rv = requests.post('http://127.0.0.1/register', json={'username': f'bob{TEST_STAMP}', 'password': 123})
    token.token = rv.json()['token']
    rv = requests.post(LOCATION_B + '/Echo', json={'token': token.token, 'text': 'hello'})
    assert rv.text == 'hello'
    rv = requests.post(LOCATION_B + '/Echo', json={'token': 123, 'text': 'hello'})
    assert rv.text == 'not a token'
    rv = requests.post(LOCATION_B + '/Echo', json={'text': 'hello'})
    assert rv.text == 'token missing'
    rv = requests.post(LOCATION_B + '/Echo', json={'token': token.token})
    assert rv.text == 'text missing'


def test_time():
    rv = requests.post(LOCATION_B + '/time', json={'token': token.token})
    data = rv.json()
    assert data['date'] == strftime('%d.%m.%Y')
    assert data['time'] == strftime('%H:%M')
    rv = requests.post(LOCATION_B + '/time', json={'token': 123})
    assert rv.text == 'not a token'


def test_cleanup():
    payload = {'username': f'bob{TEST_STAMP}',
               'password': '123psw',
               'exp': int(time() - 100),
               }
    delete_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    requests.post(LOCATION_A + '/authorize', json={'token': delete_token})
    rv = requests.get(LOCATION_A + '/show')
    data = rv.json()
    assert f'jim{TEST_STAMP}' not in data
