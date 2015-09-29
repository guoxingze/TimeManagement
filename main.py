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
import database
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users



class LoginHandler(webapp2.RequestHandler):
    def post(self):

        username = self.request.get('userName')

        template_values = {
            'userName':username
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'timer.html')
        self.response.out.write(template.render(path, template_values))


    def get(self):
        logging.info('test login get')
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
            # create google logout url
            logout_url = users.create_logout_url('/')
            # uid = str(user.user_id())
        else:
            self.redirect(users.create_login_url(self.request.uri))

    # read todo list 
        event_query = db.GqlQuery(r"SELECT * FROM Event WHERE user = :1 ORDER BY time DESC", str(user_name))
        event_list = list(db.to_dict(event) for event in event_query.run())
        event_list_json = json.dumps(event_list)
    # read achievements list
        completed_query = db.GqlQuery(r"SELECT * FROM CompletedEvent WHERE user = :1 ORDER BY time DESC", str(user_name))
        completed_list = list(db.to_dict(CompletedEvent) for CompletedEvent in completed_query.run())
        completed_list_json = json.dumps(completed_list)

    # read user info
        user_query = db.GqlQuery(r"SELECT tutorial FROM UsersHistory WHERE name = :1", str(user_name))
        user_query_list = list(db.to_dict(User) for User in user_query.run())
        user_query_list_json = json.dumps(user_query_list)
        if_user_exit = user_query.count()
        
    # if user not exit ,create user and set view tutorial = True
        if if_user_exit == 0:
            user_db = database.UsersHistory(name=user_name, tutorial=True)
            user_db.put()
            read_tutorial = True
        else:
            # if user exit, reat view tutorial
            read_tutorial = user_query_list[0]['tutorial']

        logging.info("read_tutorial  = %s" %read_tutorial)


        template_values = {
            'userName':user_name,
            'eventList':event_list_json,
            'completedList':completed_list_json,
            'readTutorial':read_tutorial,
            'logout':logout_url
        }
        path = os.path.join(os.path.dirname(__file__), 'view', 'timer.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', TimerHandler),
    webapp2.Route('/timer', TimerHandler, name='timer'),
], debug=True)
