#!/usr/bin/env python3

import sys
import os
import yaml
from jinja2 import Template
from urllib.parse import urlparse


def _render(d):
    with open(sys.argv[1]) as template:
        t = Template(template.read())
        print(t.render(**d))


data = None
if len(sys.argv) == 3:
    with open(sys.argv[2]) as config:
        data = yaml.load(config.read())
elif 'BACKEND_PORT' in os.environ:
    backend_uri = os.environ['BACKEND_PORT']
    backend_uri = backend_uri.replace("tcp://", "http://")
    if not backend_uri.endswith("/"):
        backend_uri = "%s/" % backend_uri

    uri = urlparse(backend_uri)

    data = {
        'backend': {
            'hostname': uri.hostname,
            'port': uri.port,
            'path': uri.path,
        }
    }
else:
    print("No linked applications and no config")
    sys.exit(-1)

if 'FORBIDDEN_PATHS' in os.environ:
    data['forbidden_paths'] = [p.strip() for p in os.environ['FORBIDDEN_PATHS'].split(';')]

_render(data)
