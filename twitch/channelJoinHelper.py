import asyncio
import random
from typing import List, Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from twitch.channelJoinListener import ChannelJoinListener
from twitch.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from twitch.joinChannelsEvent import JoinChannelsEvent


class ChannelJoinHelper():

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        verified: bool,
        timber: TimberInterface,
        usersRepository: UsersRepositoryInterface,
        sleepTimeSeconds: float = 12,
        maxChannelsToJoinIfUnverified: int = 10,
        maxChannelsToJoinIfVerified: int = 100
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not utils.isValidBool(verified):
            raise ValueError(f'verified argument is malformed: \"{verified}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 10 or sleepTimeSeconds > 20:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxChannelsToJoinIfUnverified):
            raise ValueError(f'maxChannelsToJoinIfUnverified argument is malformed: \"{maxChannelsToJoinIfUnverified}\"')
        elif maxChannelsToJoinIfUnverified < 5 or maxChannelsToJoinIfUnverified > 10:
            raise ValueError(f'maxChannelsToJoinIfUnverified argument is out of bounds: {maxChannelsToJoinIfUnverified}')
        elif not utils.isValidInt(maxChannelsToJoinIfVerified):
            raise ValueError(f'maxChannelsToJoinIfVerified argument is malformed: \"{maxChannelsToJoinIfVerified}\"')
        elif maxChannelsToJoinIfVerified < 5 or maxChannelsToJoinIfVerified > 200:
            raise ValueError(f'maxChannelsToJoinIfVerified argument is out of bounds: {maxChannelsToJoinIfVerified}')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__verified: bool = verified
        self.__timber: TimberInterface = timber
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxChannelsToJoinIfUnverified: int = maxChannelsToJoinIfUnverified
        self.__maxChannelsToJoinIfVerified: int = maxChannelsToJoinIfVerified

        self.__channelJoinListener: Optional[ChannelJoinListener] = None
        self.__isJoiningChannels: bool = False

    def joinChannels(self):
        if self.__isJoiningChannels:
            self.__timber.log('ChannelJoinHelper', 'Not starting channel join process as it has already been started!')
            return

        self.__isJoiningChannels = True
        self.__timber.log('ChannelJoinHelper', f'Starting channel join process...')
        self.__backgroundTaskHelper.createTask(self.__joinChannels())

    async def __joinChannels(self):
        channelJoinListener = self.__channelJoinListener

        if channelJoinListener is None:
            raise RuntimeError(f'channelJoinListener has not been set: \"{channelJoinListener}\"')

        allChannels: List[str] = list()
        disabledChannels: List[str] = list()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            if user.isEnabled():
                allChannels.append(user.getHandle())
            else:
                disabledChannels.append(user.getHandle())

        if len(disabledChannels) >= 1:
            self.__timber.log('ChannelJoinHelper', f'Disabled channel(s) that will not be joined: {disabledChannels}')

        if len(allChannels) == 0:
            self.__timber.log('ChannelJoinHelper', f'There are no channels to join')
            self.__isJoiningChannels = False
            return

        allChannels.sort(key = lambda userHandle: userHandle.lower())
        self.__timber.log('ChannelJoinHelper', f'Will be joining a total of {len(allChannels)} channel(s)...')

        workingChannels: List[str] = list()
        workingChannels.extend(allChannels)

        maxChannelsToJoin = self.__maxChannelsToJoinIfUnverified
        if self.__verified:
            maxChannelsToJoin = self.__maxChannelsToJoinIfVerified

        while len(workingChannels) >= 1:
            newChannelsToJoin: List[str] = list()

            while len(workingChannels) >= 1 and len(newChannelsToJoin) < maxChannelsToJoin - 1:
                userHandle = random.choice(workingChannels)
                workingChannels.remove(userHandle)
                newChannelsToJoin.append(userHandle)

            newChannelsToJoin.sort(key = lambda userHandle: userHandle.lower())

            await channelJoinListener.onNewChannelJoinEvent(JoinChannelsEvent(
                channels = newChannelsToJoin
            ))

            await asyncio.sleep(self.__sleepTimeSeconds)

        await channelJoinListener.onNewChannelJoinEvent(FinishedJoiningChannelsEvent(
            allChannels = allChannels
        ))

        self.__timber.log('ChannelJoinHelper', f'Finished joining {len(allChannels)} channel(s)')
        self.__isJoiningChannels = False

    def setChannelJoinListener(self, listener: Optional[ChannelJoinListener]):
        if listener is not None and not isinstance(listener, ChannelJoinListener):
            raise ValueError(f'listener argument is malformed: \"{listener}\"')

        self.__channelJoinListener = listener
