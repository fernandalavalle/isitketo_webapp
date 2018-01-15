import re

from google.appengine.ext import ndb


class Food(ndb.Model):
    brand = ndb.StringProperty()
    title = ndb.StringProperty()
    title_lower = ndb.ComputedProperty(lambda self: self.title.lower())
    variety = ndb.StringProperty()
    description = ndb.StringProperty()
    short_description = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    has_image = ndb.BooleanProperty()


def find_by_name(name):
    key = name_to_key(name)
    return key.get()


def name_to_key(name):
    key = name.lower()
    key = re.sub(r'[^a-z]', '-', key)
    return ndb.Key(Food, key)


def food_to_name(f):
    parts = []
    for part in (f.brand, f.title, f.variety):
        if part:
            parts.append(part)
    return ' '.join(parts)
