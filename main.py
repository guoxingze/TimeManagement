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
from google.appengine.api import users


# # serialize datastore model to JSON format
# def serialize(model):

#    allInstances = model.all() # fetching every instance of model
#    itemsList = [] #initial empty list
#    for p in allInstances:
#       d = db.to_dict(p)
#       itemsList.append(d)
#     return  json.dumps(itemsList)

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

        # check user login information
        user = users.get_current_user()
        if user:
            user_name = user.nickname()
            logout_url = users.create_logout_url('/')
            # uid = str(user.user_id())
        else:
            self.redirect(users.create_login_url(self.request.uri))

        event_query = db.GqlQuery(r"SELECT * FROM Event WHERE user = :1 ORDER BY time DESC", str(user_name))
        event_list = list(db.to_dict(event) for event in event_query.run())
        event_list_json = json.dumps(event_list)

        completed_query = db.GqlQuery(r"SELECT * FROM CompletedTomato WHERE user = :1 ORDER BY time DESC", str(user_name))
        # completed_query.get().order('date')
        completed_list = list(db.to_dict(CompletedTomato) for CompletedTomato in completed_query.run())
        completed_list_json = json.dumps(completed_list)



        logging.info(user.user_id)
        # today_achieve = api.read_achieve_today(date)
        # total_achieve = api.read_achieve_total()
        
        template_values = {
            'userName':user_name,
            'eventList':event_list_json,
            'completedList':completed_list_json,
            # 'today':today_achieve,
            # 'total':total_achieve,
            'logout':logout_url
            # 'eventList':eventList
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'timer.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', TimerHandler),
    webapp2.Route('/timer', TimerHandler, name='timer'),
], debug=True)
