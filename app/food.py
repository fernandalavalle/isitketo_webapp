import re

from google.appengine.ext import ndb


class Food(ndb.Model):
    title = ndb.StringProperty()
    title_lower = ndb.ComputedProperty(lambda self: self.title.lower())
    description = ndb.StringProperty()
    short_description = ndb.StringProperty()
    rating = ndb.IntegerProperty()


def find_by_name(name):
    key = name_to_key(name)
    return key.get()


def name_to_key(name):
    key = name.lower()
    key = re.sub(r'[^a-z]', '-', key)
    return ndb.Key(Food, key)
