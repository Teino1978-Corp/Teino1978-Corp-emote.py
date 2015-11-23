# Copyright 2011 Google Inc. All Rights Reserved.
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

#!/usr/bin/env python

import datetime
import logging
import os
import sys
import uuid
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.py import belay


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.template.loader import render_to_string

def server_url(path):
  return belay.this_server_url_prefix() + path

class EmoteData(db.Model):
  postCap = db.TextProperty()


class ViewHandler(belay.BcapHandler):
  def get(self):
    content = \
      render_to_string("emote.html", { 'url': server_url("/emote.css") })
    self.xhr_content(content, "text/html;charset=UTF-8")


class GenerateHandler(belay.BcapHandler):
  def get(self):
    emote = EmoteData()
    emote.put()
    self.bcapResponse(belay.regrant(LaunchHandler, emote))


class GenerateInstanceHandler(belay.BcapHandler):
  def get(self):
    emote = EmoteData()
    emote.put()
    self.bcapResponse({
      'launch': belay.regrant(LaunchHandler, emote),
      'icon': server_url("/tool-emote.png"), 
      'name': 'Emote'
    })


class LaunchHandler(belay.CapHandler):
  def get(self):
    self.bcapResponse({
        'page': {
          'html': server_url("/emote-belay.html"),
          'window': { 'width': 300, 'height': 250 }
        },
        'gadget': {
          'html': server_url("/view/gadget"),
          'scripts': [ server_url("/emote.js") ]
        },
        'info': { 
          'post': self.get_entity().postCap,
          'savePost': belay.regrant(LaunchHandler, self.get_entity())
        }
      })

  def put(self):
    emote = self.get_entity()
    emote.postCap = self.bcapRequest()
    emote.put()
    self.bcapNullResponse()


application = webapp.WSGIApplication(
  [(r'/cap/.*', belay.ProxyHandler),
  ('/belay/generate', GenerateHandler),
  ('/belay/generate-instance', GenerateInstanceHandler),
  ('/view/gadget', ViewHandler),
  ],
  debug=True)
  

belay.set_handlers(
  '/cap',
  [ ('/belay/launch', LaunchHandler),
  ])

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
Hide details
Change log
5199b78eb5b7 by Arjun Guha <arjun.guha> on Sep 13, 2011   Diff
emote does not use station storage caps;
emote uses bcap library
Go to: 	
Older revisions
All revisions of this file
File info
Size: 2754 bytes, 106 lines
View raw file
