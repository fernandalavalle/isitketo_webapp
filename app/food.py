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


def put(food):
    """Inserts food into the datastore."""
    food.key = food_to_key(food)
    food.put()


def update(existing_food_name, updated_food):
    """Updates food in datastore, deleting old key if the brand, title, or variety have changed."""
    existing_key = name_to_key(existing_food_name)
    new_key = food_to_key(updated_food)
    if existing_key.id() == new_key.id():
        updated_food.key = existing_key
        updated_food.put()
    else:
        existing_key.delete()
        put(updated_food)
    return updated_food


def find_by_name(name):
    key = name_to_key(name)
    return key.get()


def food_to_key(food):
    return name_to_key(food_to_name(food))


def name_to_key(name):
    """Replaces characters that are not legal in file paths by GCS or Linux/Windows.

    Ex: u'jalape\u00f1os -> jalapenos

    Args:
        name: A food name as presented to a user.

    Returns:
        A key that represents the canonical form of a food name.
    """
    key = name.lower()
    # n tilde to n.
    key = re.sub(u'\u00f1', 'n', key)
    # e with an accent to e.
    key = re.sub(u'[\u00e8-\u00eb]', 'e', key)
    # Gets rid of Unicode and ASCII apostrophes.
    key = re.sub(u'\u2019', '', key)
    key = re.sub(r'\'', '', key)
    key = re.sub('&', '-and-', key)
    # Get rid of ".
    key = re.sub(u'[\u201c-\u201d]', '', key)
    # Unicode dashes to ASCII dashes.
    key = re.sub(u'[\u2010-\u2015]', '-', key)
    # Make all other symbols into -.
    key = re.sub(r'[^-\d\w%\']|\s|_', '-', key)
    # Collapse neighboring hyphens into one.
    key = re.sub(r'-{2,}', '-', key)
    # Get rid of trailing or leading symbols.
    key = re.sub(r'^[^\d\w]|[^\d\w]$', '', key)
    return ndb.Key(Food, key)


def food_to_name(food):
    parts = []
    for part in (food.brand, food.title, food.variety):
        if part:
            parts.append(part)
    return ' '.join(parts)
