import requests
import partC
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


def test_start():
    rv = requests.post('http://127.0.0.1/register', json={'username': f'bob{TEST_STAMP}', 'password': 123})
    token.token = rv.json()['token']


def test_online():
    check = partC.check_address(LOCATION_A, 'token server')
    assert check is True
    check = partC.check_address(LOCATION_A, 'false')
    assert check is False
    check = partC.check_address(LOCATION_B, 'communication server')
    assert check is True
    check = partC.check_address(LOCATION_B, 'false')
    assert check is False


def test_address_check():
    adr = partC.http_check('127.0.0.1')
    assert adr == 'http://127.0.0.1'
    adr = partC.http_check('http://127.0.0.1')
    assert adr == 'http://127.0.0.1'


def test_echo():
    result = partC.echo(LOCATION_B, token.token, text='my text')
    assert result == 'my text'
    result = partC.echo(LOCATION_B, 'token.token', text='my text')
    assert result == 'not a token'


def test_time():
    result = partC.time(LOCATION_B, token.token)
    assert result == f'Server data:\t{strftime("%d.%m.%Y")}\nServer time:\t{strftime("%H:%M")}'


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
