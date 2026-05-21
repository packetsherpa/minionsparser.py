FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
COPY docker/alpine-cron/run.sh /root/
COPY minionsparser.py /etc/periodic/daily/minionsparser.py
RUN chmod +x /root/run.sh
RUN chmod +x /etc/periodic/daily/minionsparser.py
VOLUME /tmp/minionsparser
CMD ["/root/run.sh"]
