FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install requests
COPY docker/alpine-cron/run.sh /root/
COPY minionsparser.py /etc/periodic/daily/minionsparser.py
RUN chmod +x /root/run.sh
RUN chmod +x /etc/periodic/daily/minionsparser.py
VOLUME /tmp/minionsparser
CMD ["/root/run.sh"]
