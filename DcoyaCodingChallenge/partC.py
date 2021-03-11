import requests


class Data:
    """
    | class to keep servers and token data
    """
    def __init__(self):
        self.token_server = ''
        self.communication_server = ''
        self.token = ''


saved_data = Data()


def offline_wrapper(function):
    """
    | handle when token server is unreachable
    :param function: function to wrap
    :return: function or 'Server unreachable' when unreachable
    """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except requests.exceptions.ConnectionError and requests.exceptions.ConnectTimeout:
            return 'Server unreachable'
    return wrapper


@offline_wrapper
def echo(adr, token, text=None):
    """
    | echo text with the server
    :param adr: server address
    :param token: user token
    :param text: str to send to the server, default None
    :return: str, server echo respond
    """
    if text is None:
        text = input('Text to send:\n')
    rv = requests.post(adr + '/Echo', json={'token': token, 'text': text})
    return rv.text


@offline_wrapper
def time(adr, token):
    """
    | get server time
    :param adr: server address
    :param token: user token
    :return: str, server time
    """
    rv = requests.post(adr + '/time', json={'token': token}).json()
    return f'Server data:\t{rv["date"]}\nServer time:\t{rv["time"]}'


def check_address(adr, response):
    """
    | check the address is for the right server
    :param adr: server address
    :param response: respond to expect for the server
    :return: True when the server was reached
    """
    try:
        rv = requests.get(adr)
        if rv.text == response:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False


def http_check(adr):
    """
    | check for 'http://' and add when missing
    :param adr: address to check
    :return: valid address
    """
    if 'http://' not in adr:
        return 'http://' + adr
    return adr


def get_address(server):
    """
    | get the server address
    :param server: server to ask the address for
    :return: server address
    """
    while True:
        adr = input(f"Please enter the {server} address\n")
        adr = http_check(adr)
        if check_address(adr, server):
            return adr
        print(f'Cant find the server at the given address {adr}.\n'
              'Incorrect address or server offline.\n')


def get_token():
    """
    | get token from the token server, to be used in the program
    :return: token, False when the server is unreachable
    """
    while True:
        username = input('Enter username:')
        psw = input('Enter password:')
        try:
            rv = requests.post(saved_data.token_server + '/register', json={'username': username, 'password': psw})
            return rv.json()['token']
        except requests.exceptions.ConnectionError:
            return False


def keyword_wait():
    """
    | ask for user keyword for what action to take
    """
    while True:
        task = input('waiting for action keyword\n').lower().split(' ', 1)
        if task[0] == 'echo':
            print(echo(saved_data.communication_server, saved_data.token) if len(task) == 1
                  else echo(saved_data.communication_server, saved_data.token, task[1]))
        elif task[0] == 'time':
            print(time(saved_data.communication_server, saved_data.token))
        elif task[0] == 'exit':
            exit()


def start():
    """
    | setup needed values for the program
    """
    saved_data.token_server = get_address('token server')
    saved_data.communication_server = get_address('communication server')
    saved_data.token = get_token()
    if saved_data.token is False:
        print('Token server offline')
        return
    keyword_wait()


if __name__ == '__main__':
    start()
