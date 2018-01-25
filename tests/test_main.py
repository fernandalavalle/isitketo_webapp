import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from app import main
from app import subscriber


class MainTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

        main.app.testing = True
        self.client = main.app.test_client()

    def tearDown(self):
        self.testbed.deactivate()

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(200, r.status_code)

    def test_unknown_food_returns_404(self):
        r = self.client.get('/madeupfood')
        self.assertEqual(404, r.status_code)

    def test_add_subscriber_stores_valid_values(self):
        r = self.client.post(
            '/api/subscribe',
            data={
                'email': 'fakeemail@email.fake',
                'food-name': 'Fried Warbles',
            })
        self.assertEqual(200, r.status_code)
        subscribers = subscriber.SubscriberModel.query().fetch()
        self.assertEqual(1, len(subscribers))
        s = subscribers[0]
        self.assertEqual('fakeemail@email.fake', s.email)
        self.assertEqual('Fried Warbles', s.food_name)

    def test_add_subscriber_rejects_invalid_email(self):
        r = self.client.post(
            '/api/subscribe',
            data={
                'email': 'invalid@email',
                'food-name': 'hamburgers',
            })
        self.assertEqual(400, r.status_code)

    def test_add_subscriber_rejects_missing_email(self):
        r = self.client.post(
            '/api/subscribe', data={
                'food-name': 'hamburgers',
            })
        self.assertEqual(400, r.status_code)

    def test_add_subscriber_rejects_invalid_food_name(self):
        r = self.client.post(
            '/api/subscribe',
            data={
                'email': 'real@email.fake',
                'food-name': '',
            })
        self.assertEqual(400, r.status_code)

    def test_add_subscriber_rejects_missing_food_name(self):
        r = self.client.post(
            '/api/subscribe', data={
                'email': 'real@email.fake',
            })
        self.assertEqual(400, r.status_code)
