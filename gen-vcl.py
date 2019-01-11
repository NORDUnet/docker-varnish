#!/usr/bin/env python

from jinja2 import Template
import yaml
import sys
import os
from urlparse import urlparse

def _render(d):
    with open(sys.argv[1]) as template:
        t = Template(template.read())
        print t.render(**d)


data = None
if len(sys.argv) == 3:
     with open(sys.argv[2]) as config:
         data = yaml.load(config.read())
elif 'BACKEND_PORT' in os.environ:
    backend_uri = os.environ['BACKEND_PORT']
    backend_uri = backend_uri.replace("tcp://","http://")
    if not backend_uri.endswith("/"):
        backend_uri = "%s/" % backend_uri
    public_name = 'localhost'
    backends=dict(backend=[backend_uri])
    data = dict(domain='localdomain',vhosts=dict(),default_backend='backend')
    if 'ACME_PORT' in os.environ:
       acme_uri = os.environ['ACME_PORT']
       acme_uri = acme_uri.replace("tcp://","http://")
       if not acme_uri.endswith("/"):
           acme_uri = "%s/" % acme_uri
       backends['acme'] = [acme_uri]
       data['acme_backend'] = 'acme'
    data['backends'] = backends
else:
    print "No linked applications and no config" 
    sys.exit(-1)

data['uris'] = dict()
for name,members in data['backends'].iteritems():
    for member in members:
        data['uris'][member] = urlparse(member)

data['forbidden_paths'] = []
if 'FORBIDDEN_PATHS' in os.environ:
    data['forbidden_paths'] = [p.strip() for p in os.environ['FORBIDDEN_PATHS'].split(';')]

_render(data)
