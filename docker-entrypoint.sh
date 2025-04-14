#!/bin/sh

. /etc/os-release

ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

if [ "x$ID" = "xdebian" ]; then
  sed -i -e "s/# $LC_ALL UTF-8/$LC_ALL UTF-8/" /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales
fi

chown -R cynanbot:cynanbot /cynanbot/config
chown -R cynanbot:cynanbot /cynanbot/db
chown -R cynanbot:cynanbot /cynanbot/logs

gosu cynanbot:cynanbot python /cynanbot/CynanBot/initCynanBotBackend.py