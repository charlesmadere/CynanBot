import asyncio
import random
from asyncio import AbstractEventLoop
from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from twitch.channelJoinListener import ChannelJoinListener
from twitch.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from twitch.joinChannelsEvent import JoinChannelsEvent
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

        self.__isJoiningChannels: bool = False

    def joinChannels(self):
        if self.__isJoiningChannels:
            self.__timber.log('ChannelJoinHelper', 'Not starting channel join process as it has already been started!')
            return

        self.__isJoiningChannels = True
        self.__timber.log('ChannelJoinHelper', f'Starting channel join process...')
        self.__eventLoop.create_task(self.__joinChannels())

    async def __joinChannels(self):
        allChannels: List[str] = list()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            allChannels.append(user.getHandle())

        if len(allChannels) == 0:
            self.__timber.log('ChannelJoinHelper', f'There are no channels to join')
            self.__isJoiningChannels = False
            return

        allChannels.sort(key = lambda userHandle: userHandle.lower())
        self.__timber.log('ChannelJoinHelper', f'Will be joining a total of {len(allChannels)} channel(s)...')

        workingChannels: List[str] = list()
        workingChannels.extend(allChannels)

        while len(workingChannels) >= 1:
            newChannelsToJoin: List[str] = list()

            while len(workingChannels) >= 1 and len(newChannelsToJoin) < self.__maxChannelsToJoin - 1:
                userHandle = random.choice(workingChannels)
                workingChannels.remove(userHandle)
                newChannelsToJoin.append(userHandle)

            newChannelsToJoin.sort(key = lambda userHandle: userHandle.lower())

            await self.__channelJoinListener.onNewChannelJoinEvent(JoinChannelsEvent(
                channels = newChannelsToJoin
            ))

            await asyncio.sleep(self.__sleepTimeSeconds)

        await self.__channelJoinListener.onNewChannelJoinEvent(FinishedJoiningChannelsEvent(
            allChannels = allChannels
        ))

        self.__timber.log('ChannelJoinHelper', f'Finished joining {len(allChannels)} channel(s)')
        self.__isJoiningChannels = False
