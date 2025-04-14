FROM python:3.12-alpine

LABEL maintainer="CynanBot Dev Team"
LABEL org.opencontainers.image.authors="CynanBot Dev Team"
LABEL org.opencontainers.image.title="CynanBot Backend containerized install"
LABEL org.opencontainers.image.url="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.source="https://github.com/charlesmadere/CynanBot"
LABEL org.opencontainers.image.documentation="https://github.com/charlesmadere/CynanBot"

# pull latest gosu to shed privileges
ENV GOSU_VERSION=1.17

RUN apk add --no-cache --virtual .gosu-deps ca-certificates dpkg gnupg \
	&& dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
	&& wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
	&& wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
	&& gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
	&& gpgconf --kill all \
	&& rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc \
	&& apk del --no-network .gosu-deps \
	&& chmod +x /usr/local/bin/gosu

ENV UID=1000 GID=1000

# TZ & locales defaults
ENV TZ=Europe/Rome
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

COPY . /cynanbot/CynanBot
RUN apk add --no-cache jemalloc musl-utils musl-locales tzdata tini \
    && addgroup -g ${GID} cynanbot \
    && adduser -h /cynanbot -s /bin/false -D -G cynanbot -u ${UID} cynanbot \
    && chown -R cynanbot:cynanbot /cynanbot

WORKDIR /cynanbot/CynanBot

RUN pip install -r requirements-backend.txt

VOLUME ["/cynanbot/config", "/cynanbot/db", "/cynanbot/logs"]

ENV LD_PRELOAD=/usr/lib/libjemalloc.so.2
ENTRYPOINT ["/sbin/tini", "--", "/cynanbot/CynanBot/docker-entrypoint.sh"]
