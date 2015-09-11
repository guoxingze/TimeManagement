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

class Event(db.Model):
    name = db.StringProperty(required=True)

class CompletedTomato(db.Model):
    name = db.StringProperty(required=True)
    time = db.StringProperty(required=False)
    date = db.StringProperty(required=False)

def read_achieve_today():
    """
    read today's achievements count
    """
    today_date = str(datetime.now().strftime('%Y-%m-%d'))
    # query = db.GqlQuery(r"SELECT name FROM CompletedTomato WHERE time LIKE '%s'" % today_date)
    query = db.GqlQuery(r"SELECT name FROM CompletedTomato WHERE date = :1", today_date)
    results = query.count()
    logging.info("count = %s" % query.count())
    return results

def read_achieve_total():
    """
    read total achievements count
    """
    query = db.GqlQuery(r"SELECT name FROM CompletedTomato")
    results = query.count()
    logging.info("count = %s" % query.count())
    return results



class CompletedEventHandler(webapp2.RequestHandler):
    """
    Save completed event to DB
    """
    def get(self):
        logging.info('test completed_event_handler get')

    def post(self):
        logging.info(self.request.body)

        today_achieve = read_achieve_today()
        total_achieve = read_achieve_total()
        data = json.loads(self.request.body)
        eventName = data['eventName']

        if eventName == "":
            eventName = "No Event Name"

# TODO change time zone
        completedTime = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
        completedDate = str(datetime.now().strftime('%Y-%m-%d'))
        completedEvent = CompletedTomato(name = eventName,
                                         time = completedTime,
                                         date = completedDate)
        completedEvent.put()

        today_achieve += 1
        total_achieve += 1
        self.response.out.write(json.dumps(({'name': completedEvent.name,'time':completedEvent.time,
                                            'total':total_achieve,'today':today_achieve})))


        # test
        # logging.info("today = %s " % read_today())
        # logging.info("total = %s " % read_total())

class SaveEventHandler(webapp2.RequestHandler):
    """
    save event to to do list
    """
    def get(self):
        logging.info('test save get')

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        eventName = data['eventName']

        event = Event(name=eventName)
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
        eventName = data['eventName']
        logging.info("delete event name = %s" % eventName)


        logging.info(r"SELECT * FROM Event WHERE name = '%s'" % eventName)
        query = db.GqlQuery(r"SELECT * FROM Event WHERE name = '%s'" % eventName)
        results = query.fetch(1)
        db.delete(results)

        self.response.out.write(json.dumps(({'story': 42})))

app = webapp2.WSGIApplication([
    webapp2.Route('/api/save', SaveEventHandler, name='login'),
    webapp2.Route('/api/delete', DeleteEventHandler, name='login'),
    webapp2.Route('/api/complete', CompletedEventHandler, name='login'),
], debug=True)
