from datetime import datetime
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
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_modified_time = ndb.DateTimeProperty(auto_now=True)


def _sanitize_food_name(food_name):
    return re.sub(r'[^a-zA-Z\-\.\s&*\+:0-9]', '', food_name)


def put(food):
    """Inserts food into datastore."""
    food.key = food_to_key(food)
    food.put()


def update(existing_food_name, food_props):
    """Updates food in datastore, deleting old key if the brand, title, or variety have changed."""
    updated_food = update_food_props(find_by_name(existing_food_name), food_props)

    existing_key = name_to_key(existing_food_name)
    new_key = food_to_key(updated_food)

    if existing_key.id() == new_key.id():
        updated_food.put()
    else:
        existing_key.delete()
        put(updated_food)
    return updated_food


def update_food_props(food, food_props):
    """Updates the properties for a Food object based on food_props dictionary key-values."""
    for key in food_props:
        setattr(food, key, food_props[key])
    return food


def find_by_name(name):
    key = name_to_key(_sanitize_food_name(name))
    return key.get()


def food_to_key(food):
    return name_to_key(food_to_name(food))


def name_to_key(name):
    key = name.lower()
    key = re.sub(r'[^a-z]', '-', key)
    return ndb.Key(Food, key)


def food_to_name(food):
    parts = []
    for part in (food.brand, food.title, food.variety):
        if part:
            parts.append(part)
    return ' '.join(parts)
