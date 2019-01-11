#!/bin/sh

/gen-vcl.py vcl.j2 $CONFIG > /etc/varnish/default.vcl
. /etc/default/varnish
varnishd -F $DAEMON_OPTS
