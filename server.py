# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import argparse
import random
import os
import json

import gevent
import gevent.pywsgi

from time import sleep
from threading import Thread, Event

from ws4py.server.geventserver import WebSocketWSGIApplication, \
     WebSocketWSGIHandler, WSGIServer
from ws4py.websocket import EchoWebSocket

class BroadcastWebSocket(EchoWebSocket):
    def opened(self):
        app = self.environ['ws4py.app']
        app.clients.append(self)

    def received_message(self, m):
        # self.clients is set from within the server
        # and holds the list of all connected servers
        # we can dispatch to
        # app = self.environ['ws4py.app']
        # for client in app.clients:
        #     client.send(m)
        pass

    def closed(self, code, reason="A client left the room without a proper explanation."):
        app = self.environ.pop('ws4py.app')
        if self in app.clients:
            app.clients.remove(self)

class EchoWebSocketApplication(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = WebSocketWSGIApplication(handler_cls=BroadcastWebSocket)

        # keep track of connected websocket clients
        # so that we can brodcasts messages sent by one
        # to all of them. Aren't we cool?
        self.clients = []

    def __call__(self, environ, start_response):
        """
        Good ol' WSGI application. This is a simple demo
        so I tried to stay away from dependencies.
        """
        if environ['PATH_INFO'] == '/favicon.ico':
            return self.favicon(environ, start_response)

        if environ['PATH_INFO'] == '/ws':
            environ['ws4py.app'] = self
            return self.ws(environ, start_response)

        return self.webapp(environ, start_response)

    def favicon(self, environ, start_response):
        """
        Don't care about favicon, let's send nothing.
        """
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return ""

    def webapp(self, environ, start_response):
        """
        Our main webapp that'll display the chat form
        """
        status = '200 OK'
        headers = [('Content-type', 'text/html')]

        start_response(status, headers)

        return """<html>
        <head>
        <script type='application/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>
          <script type='application/javascript'>
            $(document).ready(function() {
              websocket = 'ws://%(host)s:%(port)s/ws';
              if (window.WebSocket) {
                ws = new WebSocket(websocket);
              }
              else if (window.MozWebSocket) {
                ws = MozWebSocket(websocket);
              }
              else {
                console.log('WebSocket Not Supported');
                return;
              }
              window.onbeforeunload = function(e) {
                 if(!e) e = window.event;
                 e.stopPropagation();
                 e.preventDefault();
              };
              ws.onmessage = function (evt) {
                 $('#chat').val($('#chat').val() + evt.data + '\\n');
                 $('#chat')[0].scrollTop = 999999999;
              };
              ws.onopen = function() {
                 ws.send("%(username)s entered the room");
              };
              ws.onclose = function(evt) {
                 $('#chat').val($('#chat').val() + 'Connection closed by server: ' + evt.code + ' \"' + evt.reason + '\"\\n');
              };
              $('#send').click(function() {
                 console.log($('#message').val());
                 ws.send('%(username)s: ' + $('#message').val());
                 $('#message').val("");
                 return false;
              });
            });
          </script>
        </head>
        <body>
        <form action='#' id='chatform' method='get'>
          <textarea id='chat' cols='50' rows='20'></textarea>
          </form>
        </body>
        </html>
        """ % {'username': "User%d" % random.randint(0, 100),
               'host': self.host,
               'port': self.port}



class Server(object):
    def __init__(self, host='127.0.0.1', port=9001):
        self.port = port
        self.host = host

        self.application = EchoWebSocketApplication(host, port)
        self.kill_event = Event()
        self.run_thread = Thread(target=Server.run_server, args=(host, port, self.application, self.kill_event))

    def start(self):
        self.run_thread.start()

    def stop(self):
        self.kill_event.set()

    def clients(self):
        return self.application.clients

    @staticmethod
    def run_server(host, port, application, kill_event):
        server = WSGIServer((host, port), application)
        server.start()
        while not kill_event.is_set():
            sleep(0.1)

    def send(self, data):
        data_string = json.dumps(data)
        for client in self.application.clients:
            client.send(data_string)

if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()