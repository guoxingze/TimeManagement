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
import database
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import stats
from google.appengine.api import users



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

class UpdateTutorial(webapp2.RequestHandler):
    """
    update if view tutorial to user DB
    """

    def put(self):
        """
        update tutorial in user db
        """
        data = json.loads(self.request.body)
        if_view = data['ifView']

        uid = users.get_current_user().nickname()
        user_query = db.GqlQuery(r"SELECT * FROM UsersHistory WHERE name = :1", str(uid))

        record = user_query[0]
        record.tutorial = if_view
        record.put()


class CompletedEventHandler(webapp2.RequestHandler):
    """
    cinoketed event handler
    """
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

# get user name
        uid = users.get_current_user().nickname()
        completed_event = database.CompletedEvent(name = event_name, 
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

    def post(self):
        """
        Create and dave a new event
        """
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        event_name = data['eventName']
        current_time = data['time']
        uid = users.get_current_user().nickname()
        event = database.Event(name=event_name, user=uid, time=current_time)
        event.put()

        self.response.out.write(json.dumps(({'success': True})))

class DeleteEventHandler(webapp2.RequestHandler):

    def put(self):
        """
        Delete event
        """
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        event_name = data['eventName']

        query = db.GqlQuery(r"SELECT * FROM Event WHERE name = '%s'" % event_name)
        results = query.fetch(1)
        db.delete(results)

        self.response.out.write(json.dumps(({'success': True})))

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
    webapp2.Route('/api/UpdateTutorial', UpdateTutorial, name='UpdateTutorial'),
], debug=True)
