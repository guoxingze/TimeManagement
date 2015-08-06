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
import api
import json
from google.appengine.ext.webapp import template
from google.appengine.ext import db



# # serialize datastore model to JSON format
# def serialize(model):

#    allInstances = model.all() # fetching every instance of model
#    itemsList = [] #initial empty list
#    for p in allInstances:
#       d = db.to_dict(p)
#       itemsList.append(d)
#     return  json.dumps(itemsList)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('Hello world!')
        logging.info('test init get')
        template_values = {
            'userName':'test'
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'home.html')
        self.response.out.write(template.render(path, template_values))

class LoginHandler(webapp2.RequestHandler):
    def post(self):

        username = self.request.get('userName')
        logging.info("username = "+username)

        template_values = {
            'userName':username
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'timer.html')
        self.response.out.write(template.render(path, template_values))


    def get(self):
        logging.info('test login get')
        # self.response.write('Hello world!')
        template_values = {
            'userName':'test'
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'home.html')
        self.response.out.write(template.render(path, template_values))


class TimerHandler(webapp2.RequestHandler):

    def get(self):
        logging.info('test timer get')
        # self.response.write('Hello world!')
        query = db.GqlQuery("SELECT * FROM Event")
        # eventList = query.fetch(2)
        eventList = list(db.to_dict(event) for event in query.run())
        eventList2 = json.dumps(eventList)
        # eventList2 = db.to_dict(eventList)
        # logging.info(str(eventList))
        # logging.info(type(eventList))

        # for p in eventList:
        #      logging.info("%s inches tall" % (p.name))

        logging.info(len(eventList))
        # logging.info(eventList.name)
        # logging.info(type(eventList.fetch(1)))
        # logging.info(vars(eventList.fetch(1)))
        # logging.info(str(query))
        # logging.info(type(query))
        # logging.info(type(query.fetch(1)))
        # logging.info(vars(query.fetch(1)))
        # logging.info(query.fetch(1).name())

        template_values = {
            'userName':'test',
            'eventList':eventList2
            # 'eventList':eventList
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'timer.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/timer', TimerHandler, name='timer'),
], debug=True)
