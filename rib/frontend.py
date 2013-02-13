#!/usr/bin/python
import bottle

from bottle import request, route, response, run

@route('/',method='GET')
def login():
  return "Hey man i m here to check"

@route('/ActionHost', method='POST')
def 
run(host='localhost', port=8080)
