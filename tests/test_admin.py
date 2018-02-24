import mock
import unittest

from app import admin
from app import food


class PopulateFoodFromFormTest(unittest.TestCase):

    def setUp(self):

        def test_get(key):
            responses = {
                'brand': 'Foo Brand',
                'title': 'Foo Title',
                'variety': 'Foo Variety',
                'short-description': 'Foo short description.',
                'description': 'Foo long description.',
                'rating': 2,
                'has-image': True
            }
            return responses[key]

        mock_flask_request = mock.Mock(form=mock.Mock(get=test_get))
        flask_request_patch = mock.patch.object(admin.flask, 'request',
                                                mock_flask_request)
        self.addCleanup(flask_request_patch.stop)
        flask_request_patch.start()

    def test_populating_existing_food_with_no_changes(self):
        existing_food = food.Food(
            brand='Foo Brand',
            title='Foo Title',
            variety='Foo Variety',
            short_description='Foo short description.',
            description='Foo long description.',
            rating=2,
            has_image=True)

        populated_food = admin._populate_food_from_form(existing_food)

        self.assertEqual(populated_food.brand, 'Foo Brand')
        self.assertEqual(populated_food.title, 'Foo Title')
        self.assertEqual(populated_food.variety, 'Foo Variety')
        self.assertEqual(populated_food.short_description,
                         'Foo short description.')
        self.assertEqual(populated_food.description, 'Foo long description.')
        self.assertEqual(populated_food.rating, 2)
        self.assertEqual(populated_food.has_image, True)

    def test_populating_existing_food_with_changes(self):
        existing_food = food.Food(
            brand='Fi Brand',
            title='Fi Title',
            variety='Fi Variety',
            short_description='Fi short description.',
            description='Fi long description.',
            rating=3,
            has_image=False)

        populated_food = admin._populate_food_from_form(existing_food)

        self.assertEqual(populated_food.brand, 'Foo Brand')
        self.assertEqual(populated_food.title, 'Foo Title')
        self.assertEqual(populated_food.variety, 'Foo Variety')
        self.assertEqual(populated_food.short_description,
                         'Foo short description.')
        self.assertEqual(populated_food.description, 'Foo long description.')
        self.assertEqual(populated_food.rating, 2)
        self.assertEqual(populated_food.has_image, True)
