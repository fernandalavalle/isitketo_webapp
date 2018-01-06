from google.appengine.ext import ndb


class Food(ndb.Model):
    title = ndb.StringProperty()
    title_lower = ndb.ComputedProperty(lambda self: self.title.lower())
    image_url = ndb.StringProperty()
    description = ndb.StringProperty()
    rating = ndb.IntegerProperty()
