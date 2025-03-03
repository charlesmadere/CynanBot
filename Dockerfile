FROM python:3.12-alpine

LABEL maintainer="CynanBot Dev Team"
LABEL org.opencontainers.image.authors="CynanBot Dev Team"
LABEL org.opencontainers.image.title="CynanBot Backend containerized install"
LABEL org.opencontainers.image.url="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.source="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.documentation="https://github.com/charlesmadere/CynanBot"

ENV UID=1000 GID=1000

COPY . /cynanbot/CynanBot
RUN apk add --no-cache jemalloc \
    && addgroup -g ${GID} cynanbot \
    && adduser -h /cynanbot -s /bin/false -D -G cynanbot -u ${UID} cynanbot \
    && chown -R cynanbot:cynanbot /cynanbot

USER cynanbot
WORKDIR /cynanbot/CynanBot

RUN pip install -r requirements-backend.txt

VOLUME ["/cynanbot/config", "/cynanbot/db", "/cynanbot/logs"]

ENV LD_PRELOAD=/usr/lib/libjemalloc.so.2
CMD ["python", "/cynanbot/CynanBot/initCynanBotBackend.py"]