from flask import Flask, request, jsonify
import requests
import logging
from time import strftime

APP_B = Flask(__name__)


def app_log(msg):
    """
    | ping check to see if the server is online
    :return: str, identifier
    """
    APP_B.logger.info(f'{request.remote_addr} {msg}')


def check_token(function):
    """
    | wrapper for server request function
    | catch when using with out a valid token
    :param function: warped function
    :return: function
    """
    def wrapper(*args, **kwargs):
        try:
            token = request.get_json()['token']
            rv = requests.post('http://127.0.0.1/authorize', json={'token': token})
            if rv.text == 'valid':
                return function(*args, **kwargs)
            app_log(f'Tried using {function.__name__} with invalid token')
            return rv.text
        except KeyError:
            app_log(f'Tried using {function.__name__} without a token')
            return 'token missing'
        except requests.exceptions.ConnectionError or requests.exceptions.ConnectTimeout:
            return 'Token server unreachable'

    wrapper.__name__ = function.__name__
    return wrapper


@APP_B.route('/')
def online():
    """
    | ping check to see if the server is online
    :return: str, identifier
    """
    return 'communication server'


@APP_B.route('/Echo', methods=['POST'])
@check_token
def echo():
    """
    | send given text back to the client
    :return: str, text. 'text missing' when there is no text
    """
    try:
        app_log('Used Echo')
        return request.get_json()['text']
    except KeyError:
        app_log('Used Echo with out text')
        return 'text missing'


@APP_B.route('/time', methods=['POST'])
@check_token
def send_time():
    """
    | send server time and date to the client
    :return: json, {date: x.x.x, time: x:x}
    """
    app_log('Was sent the server time')
    return jsonify(date=strftime('%d.%m.%Y'), time=strftime('%H:%M'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    # todo: port for same cpu
    APP_B.run(port=5000)
