FROM ubuntu:18.04
LABEL maintainer="Markus Krogh <markus@nordu.net>"
RUN apt-get -q update && apt-get -y upgrade && apt-get install -y varnish python3 python3-jinja2 python3-yaml
ADD settings /etc/default/varnish
ADD gen-vcl.py /gen-vcl.py
ADD vcl.j2 /vcl.j2
ENV CONFIG ""
ADD start.sh /start.sh
RUN chmod a+rx /start.sh
ENTRYPOINT ["/start.sh"]
EXPOSE 80
