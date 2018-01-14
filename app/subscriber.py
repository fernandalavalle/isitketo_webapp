from google.appengine.ext import ndb


class SubscriberModel(ndb.Model):
    timestamp = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty()
    food_name = ndb.StringProperty()
