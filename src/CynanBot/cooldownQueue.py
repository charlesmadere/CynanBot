import heapq
from datetime import datetime, timezone
from typing import Dict

import CynanBot.misc.utils as utils


class CooldownQueue():

    def __init__(self):
        self.__queue: Dict = dict()

    def addCooldown(self, channel: str, data, timeoutInSeconds):
        if not utils.isValidStr(channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')
        elif timeoutInSeconds is None:
            raise ValueError(f'timeoutInSeconds argument is malformed: \"{timeoutInSeconds}\"')

        if not channel in self.__queue:
            self.__queue[channel] = list()

        # could add dupe checking if you want it, but it's really not necessary tbh
        heapq.heappush(self.__queue[channel], (datetime.now(timezone.utc) + timeoutInSeconds, data))

    def getExpireTime(self, channel: str, data):
        if not utils.isValidStr(channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        now = datetime.now(timezone.utc)

        if not channel in self.__queue:
            self.__queue[channel] = list()

        # prune cooldowns that have expired
        for _ in range(len(self.__queue)):
            if self.__queue[channel][0][0] < now:
                heapq.heappop(self.__queue[channel])
                continue

            break

        # check if it's on cooldown
        for k, v in self.__queue[channel]:
            if v == data:
                return k - now

        # return None if there's no cooldown, could also return 0.0 or something
        return None
