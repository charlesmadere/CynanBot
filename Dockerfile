FROM python:3.12-slim

LABEL maintainer="CynanBot Dev Team"
LABEL org.opencontainers.image.authors="CynanBot Dev Team"
LABEL org.opencontainers.image.title="CynanBot Backend containerized install"
LABEL org.opencontainers.image.url="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.source="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.documentation="https://github.com/charlesmadere/CynanBot"

ENV UID=1000 GID=1000

# TZ & locales defaults
ENV TZ=Europe/Rome
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

COPY . /cynanbot/CynanBot
RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y gosu libjemalloc2 \
	   locales tzdata tini && addgroup --gid ${GID} cynanbot \
    && useradd -d /cynanbot -s /bin/false -g cynanbot -M \
	   -u ${UID} cynanbot \
    && chown -R cynanbot:cynanbot /cynanbot \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /cynanbot/CynanBot

RUN pip install -r requirements-backend.txt

VOLUME ["/cynanbot/config", "/cynanbot/db", "/cynanbot/logs"]

ENV LD_PRELOAD=libjemalloc.so.2
ENTRYPOINT ["/usr/bin/tini", "--", "/cynanbot/CynanBot/docker-entrypoint.sh"]
