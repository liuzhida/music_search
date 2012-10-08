#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
import tornado
import htmlentitydefs
import re
import sys
import urllib
class JSONPHandler(RequestHandler):
    
    CALLBACK = 'jsonp' # define callback argument name
    
    def finish(self, chunk=None):
        """Finishes this response, ending the HTTP request."""
        assert not self._finished
        if chunk: self.write(chunk)
        
        # get client callback method
        callback = tornado.escape.utf8(self.get_argument(self.CALLBACK))
        # format output with jsonp
        self._write_buffer.insert(0, callback + '(')
        self._write_buffer.append(')')
        
        # call base class finish method
        super(JSONPHandler, self).finish() # chunk must be None
