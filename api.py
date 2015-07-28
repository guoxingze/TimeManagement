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

class Pet(db.Model):
  name = db.StringProperty(required=True)
  weight_in_pounds = db.IntegerProperty()

class save_tomato_handler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('Hello world!')
        logging.info('test save get')

    def post(self):
        logging.info(self.request.body)
        time.sleep(2)

        # pet = Pet(name="Fluffy",weight_in_pounds=37)
        # pet.put();
        data = json.loads(self.request.body)
        query = db.GqlQuery("SELECT * FROM Pet WHERE weight_in_pounds < 39")
        logging.info(query)
        logging.info(query.fetch(0))
        self.response.out.write(json.dumps(({'story': 42})))

app = webapp2.WSGIApplication([
    webapp2.Route('/api/save', save_tomato_handler, name='login'),
], debug=True)
