#!/usr/bin/env python
#coding=utf-8
from BeautifulSoup import BeautifulSoup
import tornado.httpserver
import tornado.ioloop
from tornado import httpclient
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options
import helpers as h
import brukva
from brukva import adisp
import random
import database
from realtime import publish
import re
import urllib2
import urllib
import redis

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search1.html')

class SSHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @adisp.process
    def get(self):
        word = self.get_argument('word')
        word = word.encode('utf_8')
        #c = redis.Redis(host='127.0.0.1', port=6379, db=0)
        #tag = c.exists(word)
        c = database.AsyncRedis.client()
        tag = yield c.async.exists(word)
        if tag:
            value = yield c.async.zrange("%s"%word, 0, -1, False)
            #value = c.zrange(word, 0, -1)

            #c.zincrby(word, value, 1)
            data = []
            value = eval(value[0])
            for li in value:
                songname = li[2]
                singer = li[3]
                album = li[-1]
                url = "commdown('" + "','".join(li) + "');"
                result = {}
                result['songname'] = songname
                result['singer']   = singer
                result['album']    = album
                result['url']      = url 
                data.append(result)
            self.render('result2.html',li = data)
        
        #else:
            #params = urllib.urlencode({'key':'%s'%word,'pn':'','from':'hzwdx'})
            #f = urllib.urlopen("http://player.kuwo.cn/webmusic/wdx/websearch",params)
            #webdata = f.read()
            #soup = BeautifulSoup(''.join(webdata))
            #data = []
            #data1 = []
            #for i in soup.findAll(attrs = {"class":"itemUl"}):
            #    if not i.findAll(attrs = {"class":"downBtn"}):
            #        continue
            #    url = i.findAll(attrs = {"class":"downBtn"})[0]
            #    li = url['href'].split(":")[1]
            #    li = li.lstrip("commondown(").rstrip(");").replace("'","").split(",")
            #    songname = li[2]
            #    singer = li[3]
            #    album = li[-1]
            #    result = {}
            #    result['songname'] = songname
            #    result['singer']   = singer
            #    result['album']    = album
            #    result['url']      = url['href']
            #    data.append(result)
            #    data1.append(li)
            #self.render('result1.html',li = data)
            #yield c.async.zadd(word,1,data1)
            #c.zadd(word,data1,1)

class MSHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @adisp.process
    def get(self):
        word = self.get_argument('word')
        word = word.encode('utf_8')
        #c = redis.Redis(host='127.0.0.1', port=6379, db=0)
        #tag = c.exists(word)
        c = database.AsyncRedis.client()
        tag = yield c.async.exists(word)
        if tag:
            value = yield c.async.zrange("%s"%word, 0, -1, False)
            #value = c.zrange(word, 0, -1)
            
            #c.zincrby(word, value, 1)
            data = []
            value = eval(value[0])
            for li in value:
                songname = li[2]
                singer = li[3]
                album = li[-1]
                url = "commdown('" + "','".join(li) + "');"
                result = {}
                result['songname'] = songname
                result['singer']   = singer
                result['album']    = album
                result['from']     = "kuwo"
                result['url']      = url 
                data.append(result)
            json = {"result":data}
            self.finish(json)
        
        #else:
            #params = urllib.urlencode({'key':'%s'%word,'pn':'','from':'hzwdx'})
            #f = urllib.urlopen("http://player.kuwo.cn/webmusic/wdx/websearch",params)
            #webdata = f.read()
            #soup = BeautifulSoup(''.join(webdata))
            #data = []
            #data1 = []
            #for i in soup.findAll(attrs = {"class":"itemUl"}):
            #    if not i.findAll(attrs = {"class":"downBtn"}):
            #        continue
            #    url = i.findAll(attrs = {"class":"downBtn"})[0]
            #    li = url['href'].split(":")[1]
            #    li = li.lstrip("commondown(").rstrip(");").replace("'","").split(",")
            #    songname = li[2]
            #    singer = li[3]
            #    album = li[-1]
            #    result = {}
            #    result['songname'] = songname
            #    result['singer']   = singer
            #    result['album']    = album
            #    result['from']     = "kuwo"
            #    result['url']      = url['href']
            #    data.append(result)
            #    data1.append(li)
            #json = {"result":data}
            #self.finish(json)
            ##c.zadd(word,data1,1)
            #yield c.async.zadd(word,1,data1)

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('music.html')

def main():
    define("port", default=8080, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates","static_path": "static",
           "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",              IndexHandler),
        (r"/search",            SSHandler),
        (r"/api",            MSHandler),
        (r"/test",            TestHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
