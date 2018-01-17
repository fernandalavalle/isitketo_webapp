import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from app import food
from app import sitemap


class SitemapTests(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def assertXmlEqual(self, a, b):
        self.assertEqual(a.strip().replace('\n', ''),
                         b.strip().replace('\n', ''))

    def test_when_database_is_empty_returns_root_url(self):
        self.assertXmlEqual("""
<?xml version=\'1.0\' encoding=\'utf-8\'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<url>
<loc>https://isitketo.org/</loc>
</url>
</urlset>
""", sitemap.get())

    def test_when_database_has_foods_returns_food_urls(self):
        banana = food.Food(
            title='Banana',
            short_description='No, they are not keto',
            description='Not keto, too much sugar',
            rating=1)
        banana.key = food.name_to_key(food.food_to_name(banana))
        banana.put()

        diet_coke = food.Food(
            title='Diet Coke',
            short_description='So keto',
            description='Yeah, drink up!',
            rating=5)
        diet_coke.key = food.name_to_key(food.food_to_name(diet_coke))
        diet_coke.put()

        self.assertXmlEqual("""
<?xml version=\'1.0\' encoding=\'utf-8\'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<url>
<loc>https://isitketo.org/</loc>
</url>
<url>
<loc>https://isitketo.org/banana</loc>
</url>
<url>
<loc>https://isitketo.org/diet-coke</loc>
</url>
</urlset>
""", sitemap.get())
