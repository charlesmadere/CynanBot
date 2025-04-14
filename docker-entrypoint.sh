#!/bin/sh

ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

chown -R cynanbot:cynanbot /cynanbot/config
chown -R cynanbot:cynanbot /cynanbot/db
chown -R cynanbot:cynanbot /cynanbot/logs

/usr/local/bin/gosu cynanbot:cynanbot python /cynanbot/CynanBot/initCynanBotBackend.py