import unittest
import requests
import sqlite3
from flaskr import DATABASE, create_app
from flaskr.models import create_db
from os import remove

LONG_URL = 'https://www.linkedin.com/in/idotan/'


def data_from_sqldb(database=f'Backend Developer Exercise/{DATABASE}'):
    connection = sqlite3.connect(f'{database}')
    found = connection.execute(f'SELECT id,long_url,short_url,clicks FROM url WHERE long_url= "{LONG_URL}"')
    row = found.fetchall()[-1]
    connection.commit()
    connection.close()
    return row


class Test(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.test_db = 'test.db'
        app.config['DATABASE'] = self.test_db
        app.testing = True
        create_db(self.test_db)
        self.client = app.test_client()

    def tearDown(self):
        remove(self.test_db)

    def test_client(self):
        rv = self.client.post('http://localhost:8000/create', json={'url': LONG_URL})
        url_end = rv.data.decode('utf-8').split('/')[-1]
        url_db = data_from_sqldb(self.test_db)[2]
        self.assertEqual(url_end, url_db)

    def test_add_url(self):
        rv = requests.post('http://localhost:8000/create', json={'url': LONG_URL})
        url_end = rv.text.split('/')[-1]
        url_db = data_from_sqldb()[2]
        self.assertEqual(url_end, url_db)

    def test_redirect(self):
        url = data_from_sqldb()[2]
        rv = requests.get(f'http://localhost:8000/s/{url}')
        self.assertEqual(LONG_URL, rv.url)

    def test_view_count(self):
        def use_link(go_to):
            requests.get(go_to)

        data = data_from_sqldb()
        start_views = data[3]
        url = f'http://localhost:8000/s/{data[2]}'
        for i in range(5):
            use_link(url)
        new_views = data_from_sqldb()[3]
        self.assertEqual(new_views, start_views + 5)

    def test_not_url(self):
        rv = requests.get(f'http://localhost:8000/s/123')
        self.assertEqual(rv.text, 'unknown url')


if __name__ == '__main__':
    unittest.main()
