import unittest

from app import main


class MainTest(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.client = main.app.test_client()

    def test_index(self):
        r = self.client.get('/')
        assert r.status_code == 200
