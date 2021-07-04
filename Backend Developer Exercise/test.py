import unittest
import requests
import sqlite3
from flaskr.models import DATABASE

LONG_URL = 'https://www.linkedin.com/in/idotan/'


def data_from_sqldb():
    row = []
    connection = sqlite3.connect(f'Backend Developer Exercise/{DATABASE}')
    found = connection.execute(f'SELECT * FROM url WHERE long_url= "{LONG_URL}"')
    for row in found:
        row = row
    connection.commit()
    connection.close()
    return row


class Test(unittest.TestCase):
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
