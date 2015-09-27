import webapp2
from google.appengine.ext import db

# Event talbe in DB
class Event(db.Model):
    name = db.StringProperty(required=True)
    user = db.StringProperty(required=True)
    time = db.StringProperty(required=False)

# CompletedEvent talbe in DB
class CompletedEvent(db.Model):
    name = db.StringProperty(required=True)
    time = db.StringProperty(required=False)
    date = db.StringProperty(required=False)
    user = db.StringProperty(required=True)

# User DB
class UsersHistory(db.Model):
    name = db.StringProperty(required=True)
    tutorial = db.BooleanProperty(required=True)