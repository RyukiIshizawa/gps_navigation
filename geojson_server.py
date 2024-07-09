from wsgiref.simple_server import make_server

import json


def app(environ, start_response):
  status = '200 OK'
  headers = [
    ('Content-type', 'application/json; charset=utf-8'),
    ('Access-Control-Allow-Origin', '*'),
  ]
  start_response(status, headers)

  with open("gpsd.geojson") as f:
    return [json.dumps(json.load(f)).encode('utf-8')]

with make_server('', 3000, app) as httpd:
  print("Serving on port 3000...")
  httpd.serve_forever()