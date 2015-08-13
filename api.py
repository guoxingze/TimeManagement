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
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Event(db.Model):
    name = db.StringProperty(required=True)

class CompletedTomato(db.Model):
    name = db.StringProperty(required=True)
    time = db.StringProperty(required=False)


class completed_event_handler(webapp2.RequestHandler):
    """
    test docString
    """
    def get(self):
        logging.info('test completed_event_handler get')

    def post(self):
        logging.info(self.request.body)

        data = json.loads(self.request.body)
        eventName = data['eventName']

        completedEvent = CompletedTomato(name=eventName,time="2015-01-01")
        completedEvent.put()
        # query = db.GqlQuery("SELECT * FROM Pet WHERE weight_in_pounds < 39")
        # logging.info(query)
        # logging.info(query.fetch(0))
        self.response.out.write(json.dumps(({'story': 42})))


class save_event_handler(webapp2.RequestHandler):
    """
    test docString
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


class delete_event_handler(webapp2.RequestHandler):
    """
    test docString
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
    webapp2.Route('/api/save', save_event_handler, name='login'),
    webapp2.Route('/api/delete', delete_event_handler, name='login'),
    webapp2.Route('/api/complete', completed_event_handler, name='login'),
], debug=True)
