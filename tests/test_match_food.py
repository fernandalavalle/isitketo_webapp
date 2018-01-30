import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from app import food
from app import match_food


def _add_dummy_food_to_datastore(food_title):
    food.put(
        food.Food(
            title=food_title,
            short_description='dummy short description',
            rating=5,
            description='dummy long description'))


class MatchFoodTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_match_by_removing_s(self):
        _add_dummy_food_to_datastore('Egg')
        self.assertEqual('egg', match_food.match('eggs'))

    def test_match_by_removing_es(self):
        _add_dummy_food_to_datastore('Potato')
        self.assertEqual('potato', match_food.match('potatoes'))

    def test_match_by_adding_s(self):
        _add_dummy_food_to_datastore('Pecans')
        self.assertEqual('pecans', match_food.match('pecan'))

    def test_match_by_adding_es(self):
        _add_dummy_food_to_datastore('Twixes')
        self.assertEqual('twixes', match_food.match('Twix'))

    def test_match_by_replacing_y(self):
        _add_dummy_food_to_datastore('berries')
        self.assertEqual('berries', match_food.match('berry'))

    def test_match_by_replacing_ies_with_y(self):
        _add_dummy_food_to_datastore('berry')
        self.assertEqual('berry', match_food.match('berries'))
