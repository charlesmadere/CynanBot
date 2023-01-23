import asyncio
import random
from asyncio import AbstractEventLoop
from typing import List, Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from twitch.channelJoinListener import ChannelJoinListener
from users.usersRepository import UsersRepository


class ChannelJoinHelper():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        channelJoinListener: ChannelJoinListener,
        timber: Timber,
        usersRepository: UsersRepository,
        sleepTimeSeconds: float = 16,
        maxChannelsToJoin: int = 10
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(channelJoinListener, ChannelJoinListener):
            raise ValueError(f'channelJoinListener argument is malformed: \"{channelJoinListener}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 12 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxChannelsToJoin):
            raise ValueError(f'maxChannelsToJoin argument is malformed: \"{maxChannelsToJoin}\"')
        elif maxChannelsToJoin < 3 or maxChannelsToJoin > 10:
            raise ValueError(f'maxChannelsToJoin argument is out of bounds: {maxChannelsToJoin}')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__channelJoinListener: ChannelJoinListener = channelJoinListener
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxChannelsToJoin: int = maxChannelsToJoin

        self.__isStarted: bool = False
        self.__allChannels: Optional[List[str]] = None

    def startJoiningChannels(self):
        if self.__isStarted:
            self.__timber.log('ChannelJoinHelper', 'Not starting channel join loop as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('ChannelJoinHelper', f'Starting channel joining...')
        self.__eventLoop.create_task(self.__startJoiningChannelsLoop())

    async def __startJoiningChannelsLoop(self):
        while True:
            if self.__allChannels is None:
                self.__allChannels = list()
                allUsers = await self.__usersRepository.getUsersAsync()

                for user in allUsers:
                    self.__allChannels.append(user.getHandle())

                self.__timber.log('ChannelJoinHelper', f'Will be joining a total of {len(allUsers)} channel(s)...')

            channels: List[str] = list()

            while len(self.__allChannels) >= 1 and len(channels) < self.__maxChannelsToJoin - 1:
                userHandle = random.choice(self.__allChannels)
                self.__allChannels.remove(userHandle)
                channels.append(userHandle)

            if len(channels) == 0:
                self.__timber.log('ChannelJoinHelper', f'Finished joining channels')
                return

            await self.__channelJoinListener.joinChannels(channels)
            await asyncio.sleep(self.__sleepTimeSeconds)
