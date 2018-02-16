import sanitizer

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
    """Inserts food into datastore."""
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
    key = name.lower()
    key = sanitizer.food_name(key)
    return ndb.Key(Food, key)


def food_to_name(food):
    parts = []
    for part in (food.brand, food.title, food.variety):
        if part:
            parts.append(part)
    return ' '.join(parts)
