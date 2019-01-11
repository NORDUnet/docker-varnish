FROM ubuntu:18.04
LABEL maintainer="Markus Krogh <markus@nordu.net>"
RUN apt-get -q update && apt-get -y upgrade && apt-get install -y screen varnish xinetd python python-jinja2 python-yaml
ADD settings /etc/default/varnish
ADD monitor.sh /etc/varnish/monitor.sh
ADD varnish-monitor /etc/xinetd.d/varnish-monitor
ADD gen-vcl.py /gen-vcl.py
ADD vcl.j2 /vcl.j2
ENV CONFIG ""
ADD start.sh /start.sh
RUN chmod a+rx /start.sh
ENTRYPOINT ["/start.sh"]
EXPOSE 80
