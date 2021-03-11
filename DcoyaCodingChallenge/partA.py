from flask import Flask, request, jsonify
import jwt
import logging
from time import time

APP_A = Flask(__name__)
authorized = []
JWT_SECRET = 'MySecretKey'
JWT_ALGORITHM = 'HS256'
TOKEN_EXP = 3600


def app_log(msg):
    APP_A.logger.info(f'{request.remote_addr} {msg}')


@APP_A.route('/')
def online():
    """
    | ping check to see if the server is online
    :return: str, identifier
    """
    return 'token server'


@APP_A.route('/register', methods=['POST'])
def register():
    """
    | register user and assign them a token
    :return: user's token
    """
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']
    if not (username and password):
        app_log('Tried to register with missing information')
        return 'False'
    for user in authorized:
        for name, psw in user.items():
            if name == username:
                app_log('Tried to register with already registered username')
                return 'already registered'
    payload = {'username': username,
               'password': password,
               'exp': int(time() + TOKEN_EXP),
               }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    authorized.append({username: password})
    app_log('Registered with a new user')
    return jsonify(token=jwt_token)


@APP_A.route('/show')
def show():
    """
    | create user list and send it
    :return: list of all users
    """
    user_list = []
    for users in authorized:
        for user in users:
            user_list.append(user)
    # todo: ask wat is the 'list' to send
    app_log('Was sent all register users')
    return jsonify(user_list)


@APP_A.route('/authorize', methods=['POST'])
def authorize():
    """
    | check if a given token exist
    :return: valid when token exist, invalid otherwise
    """
    token = request.get_json()['token']
    try:
        token_data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        for user in authorized:
            for username, psw in user.items():
                if username == token_data['username'] and psw == token_data['password']:
                    app_log('Used a valid token')
                    return 'valid'
    except jwt.DecodeError:
        app_log('Used an invalid token')
        return 'not a token'
    except jwt.ExpiredSignatureError:
        delete_user = jwt.decode(request.get_json()['token'], JWT_SECRET, JWT_ALGORITHM, options={'verify_exp': False})
        for user in authorized:
            for username, psw in user.items():
                if username == delete_user['username']:
                    authorized.remove(user)
        app_log('Used an expired token')
        return 'expired token'
    return 'error'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    APP_A.run(port=80)
