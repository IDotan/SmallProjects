from flask import Blueprint, request, redirect, current_app
import sqlite3
from time import time
from string import ascii_lowercase, ascii_uppercase
from random import randint, shuffle

view = Blueprint('view', __name__)
ABC = ascii_lowercase+ascii_uppercase


def work_on_db(function):
    """
    | wrapper to open and close connection with the db.
    | used for function how need to work with the db.
    :param function: function to wrap
    :return: the function's return or none when there is no return
    """
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(current_app.config['DATABASE'])
        returned = function(connection, *args, **kwargs)
        connection.commit()
        connection.close()
        return returned

    wrapper.__name__ = function.__name__
    return wrapper


def random_url_end():
    """
    | create a random end to the url
    :return: str, url end
    """
    short_end = ''
    for i in range(4):
        short_end += ABC[randint(0, len(ABC) - 1)]
    time_code = str(time()).split('.')[0]
    short_end += time_code[-6:-1:2]
    short_end = list(short_end)
    shuffle(short_end)
    return ''.join(short_end)


@work_on_db
def not_in_use(cursor, url):
    """
    | make sure the url end is not used in the database
    :param cursor: sql connection object
    :param url: url end to check if it's in the database
    :return: True when not in the database
    """
    found = cursor.execute(f'SELECT short_url FROM url WHERE short_url="{url}"')
    found = found.fetchone()
    if found:
        return False
    return True


@work_on_db
def add_new_short(cursor, url, short_url):
    """
    | add new entry to the database
    :param cursor: sql connection object
    :param url: original url (url to redirect to)
    :param short_url: end of the short url
    """
    cursor.execute(f'INSERT INTO url (long_url, short_url, clicks) VALUES ("{url}", "{short_url}", 0)')


@view.route('/create', methods=['POST'])
def create_short():
    """
    | start to create and register new short url
    :return: string of the new short url
    """
    url = request.json['url']
    while True:
        url_end = random_url_end()
        if not_in_use(url_end):
            break
    add_new_short(url, url_end)
    return f'http://localhost:8000/s/{url_end}'


@work_on_db
def check_logged_url(cursor, url):
    """
    | check if the given short link is in the database
    :param cursor: sql connection object
    :param url: end of short url to check
    :return: string of the url to redirect to if found, False otherwise
    """
    found = cursor.execute(f'SELECT id,long_url,short_url,clicks FROM url WHERE short_url= "{url}"')
    found = found.fetchone()
    if found:
        id_num = found[0]
        long_url = found[1]
        clicks = found[3]
        cursor.execute(f'UPDATE url set clicks = "{clicks + 1}" WHERE id = {id_num}')
        return long_url
    return False


@view.route('/s/<url>')
def view_site(url):
    """
    | redirect to the original long url
    :param url: end of the short url
    :return: redirect to the long url, otherwise 'unknown url'
    """
    redirect_url = check_logged_url(url)
    if redirect_url:
        return redirect(redirect_url)
    return 'unknown url'
