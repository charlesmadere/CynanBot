FROM python:3.12-alpine

ENV UID=1000 GID=1000

COPY . /cynanbot/CynanBot
RUN apk add --no-cache jemalloc \
    && addgroup -g ${GID} cynanbot \
    && adduser -h /cynanbot -s /bin/false -D -G cynanbot -u ${UID} cynanbot \
    && chown -R cynanbot:cynanbot /cynanbot

USER cynanbot
WORKDIR /cynanbot/CynanBot

RUN pip install -r requirements-backend.txt

VOLUME ["/cynanbot/config", "/cynanbot/logs"]

ENV LD_PRELOAD=/usr/lib/libjemalloc.so.2
CMD ["python", "/cynanbot/CynanBot/initCynanBotBackend.py"]