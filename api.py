#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
import json
import time
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import stats
from google.appengine.api import users

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

def read_achieve_today(date):
    """
    read today's achievements count
    """
    # today_date = str(datetime.now().strftime('%Y-%m-%d'))
    # query = db.GqlQuery(r"SELECT name FROM CompletedEvent WHERE time LIKE '%s'" % today_date)
    uid = users.get_current_user().nickname()
    query = db.GqlQuery(r"SELECT name FROM CompletedEvent WHERE date = :1 and user = :2", date, uid)
    results = query.count()
    logging.info("count = %s" % query.count())
    return results

def read_achieve_total():
    """
    read total achievements count
    """
    uid = users.get_current_user().nickname()
    query = db.GqlQuery(r"SELECT name FROM CompletedEvent WHERE user = :1", uid)
    results = query.count()
    logging.info("count = %s" % query.count())
    return results

class update_tutorial(webapp2.RequestHandler):
    """
    update if view tutorial to user DB
    """

    def put(self):
        data = json.loads(self.request.body)
        if_view = data['ifView']
        logging.info("if_view = %s" %if_view)

        uid = users.get_current_user().nickname()
        user_query = db.GqlQuery(r"SELECT * FROM UsersHistory WHERE name = :1", str(uid))
        user_query_list = list(db.to_dict(User) for User in user_query.run())
        # user_query_list_json = json.dumps(user_query_list)
        record = user_query[0]
        record.tutorial = if_view
        logging.info(user_query)
        logging.info(user_query[0].name)
        record.put()
        # logging.debug(record)
        # record.tutorial = if_view
        # This updates it
        # record.put()



class CompletedEventHandler(webapp2.RequestHandler):
    """
    Save completed event to DB
    """
    def get(self):
        logging.info('test completed_event_handler get')

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        event_name = data['eventName']
        current_time = data['time']

# read the achievements before compplete event
        today_achieve = read_achieve_today(current_time[:10])
        total_achieve = read_achieve_total()

        if event_name == "":
            event_name = "No Event Name"


        uid = users.get_current_user().nickname()
        completed_event = CompletedEvent(name = event_name, 
                                         time = current_time[:16], 
                                         date = current_time[:10],   #only input yyyy-mm-dd into db date field
                                         user = uid)
        completed_event.put()

        today_achieve += 1
        total_achieve += 1
        self.response.out.write(json.dumps(({'name': completed_event.name,'time':completed_event.time,
                                            'total':total_achieve,'today':today_achieve})))



class SaveEventHandler(webapp2.RequestHandler):
    """
    save event to to do list
    """
    def get(self):
        logging.info('test save get')

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        event_name = data['eventName']
        current_time = data['time']
        uid = users.get_current_user().nickname()
        event = Event(name=event_name, user=uid, time=current_time)
        event.put()
        # query = db.GqlQuery("SELECT * FROM Pet WHERE weight_in_pounds < 39")
        # logging.info(query)
        # logging.info(query.fetch(0))
        self.response.out.write(json.dumps(({'story': 42})))



class DeleteEventHandler(webapp2.RequestHandler):
    """
    delete event from to do list
    """
    def get(self):
        logging.info('test save get')

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        event_name = data['eventName']
        logging.info("delete event name = %s" % event_name)


        logging.info(r"SELECT * FROM Event WHERE name = '%s'" % event_name)
        query = db.GqlQuery(r"SELECT * FROM Event WHERE name = '%s'" % event_name)
        results = query.fetch(1)
        db.delete(results)

        self.response.out.write(json.dumps(({'story': 42})))

class UpdateAchieveHandler(webapp2.RequestHandler):
    """
    read current achievenment and return to front end
    """

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        current_time = data['time']
        logging.info("current date = %s" % current_time)

        today_achieve = read_achieve_today(current_time[:10])
        total_achieve = read_achieve_total()

        self.response.out.write(json.dumps(({'today': today_achieve, 'total': total_achieve})))

app = webapp2.WSGIApplication([
    webapp2.Route('/api/save', SaveEventHandler, name='save'),
    webapp2.Route('/api/delete', DeleteEventHandler, name='delete'),
    webapp2.Route('/api/complete', CompletedEventHandler, name='complete'),
    webapp2.Route('/api/update_achieve', UpdateAchieveHandler, name='update_achieve'),
    webapp2.Route('/api/update_tutorial', update_tutorial, name='update_tutorial'),
], debug=True)
