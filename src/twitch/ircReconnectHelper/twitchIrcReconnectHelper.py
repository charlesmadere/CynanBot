import asyncio
import traceback
from dataclasses import dataclass
from typing import Any, Collection, Final

from frozendict import frozendict
from frozenlist import FrozenList
from twitchio import Channel
from twitchio.ext.commands import Bot

from .twitchIrcReconnectHelperInterface import TwitchIrcReconnectHelperInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchIrcReconnectHelper(TwitchIrcReconnectHelperInterface):

    @dataclass(frozen = True)
    class TwitchUserData:
        userId: str
        userName: str

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        sleepTimeSeconds: float = 150.0,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 30 or sleepTimeSeconds > 600:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds

        self.__isStarted: bool = False
        self.__twitchIoBot: Bot | None = None

    async def __checkIrcConnections(self, twitchIoBot: Bot):
        if not isinstance(twitchIoBot, Bot):
            raise TypeError(f'twitchIoBot argument is malformed: \"{twitchIoBot}\"')

        enabledUsers = await self.__getEnabledUsers()

        if len(enabledUsers) == 0:
            # this would be an extremely bizarre state, but let's just be safe
            return

        await twitchIoBot.wait_for_ready()

        disconnectedUsers = await self.__getDisconnectedUsers(
            twitchIoBot = twitchIoBot,
            enabledUsers = enabledUsers,
        )

        if len(disconnectedUsers) == 0:
            self.__timber.log('TwitchIrcReconnectHelper', f'All {len(enabledUsers)} user(s) are connected to IRC')
            return

        self.__timber.log('TwitchIrcReconnectHelper', f'Found {len(disconnectedUsers)} disconnected user(s) out of {len(enabledUsers)} total user(s), reconnecting now ({disconnectedUsers=})...')

        disconnectedUserNames: list[str] = [ user.userName for user in disconnectedUsers ]

        try:
            # This call might not be necessary, I'm not really sure. It depends on
            # if the Twitch IO library is actually aware of the fact of its dead IRC
            # connection(s). But whatever, let's just manually disconnect from these
            # channels before reconnecting to them.
            await twitchIoBot.part_channels(disconnectedUserNames)
        except Exception as e:
            # This try/catch block is probably a bit extraneous, but whatever. I want
            # to keep this just in case the Twitch IO library goes haywire when telling
            # it to part from channels that we're already disconnected from.
            self.__timber.log('TwitchIrcReconnectHelper', f'Encountered unknown Exception when parting from Twitch channel(s) before attempting to reconnect', e, traceback.format_exc())

        await twitchIoBot.join_channels(disconnectedUserNames)
        self.__timber.log('TwitchIrcReconnectHelper', f'Finished IRC reconnections! ({disconnectedUsers=})')

    async def __getDisconnectedUsers(
        self,
        twitchIoBot: Bot,
        enabledUsers: frozendict[str, TwitchUserData],
    ) -> FrozenList[TwitchUserData]:
        if not isinstance(twitchIoBot, Bot):
            raise TypeError(f'twitchIoBot argument is malformed: \"{twitchIoBot}\"')
        elif not isinstance(enabledUsers, frozendict):
            raise TypeError(f'enabledUsers argument is malformed: \"{enabledUsers}\"')

        enabledUserIds: frozenset[str] = frozenset(enabledUsers.keys())
        connectedUserIds: set[str] = set()

        # don't trust type hints from this library
        connectedChannels: Collection[Channel] | Any | None = twitchIoBot.connected_channels

        if isinstance(connectedChannels, Collection):
            for connectedChannel in connectedChannels:
                try:
                    connectedUserId = await self.__userIdsRepository.requireUserId(
                        userName = connectedChannel.name,
                    )
                except NoSuchUserException as e:
                    self.__timber.log('TwitchIrcReconnectHelper', f'Failed to fetch user ID for connected channel ({connectedChannel=})', e, traceback.format_exc())
                    continue

                if connectedUserId in enabledUserIds:
                    connectedUserIds.add(connectedUserId)
                else:
                    # This would mean we are connected to a channel that we shouldn't be. I guess
                    # this should definitely be impossible, but let's just log it for now.
                    self.__timber.log('TwitchIrcReconnectHelper', f'Discovered a channel that we\'re connected to, but it isn\'t in the enabled users list ({connectedChannel=}) ({connectedUserId=}) ({enabledUsers=})')

        disconnectedUsers: FrozenList[TwitchIrcReconnectHelper.TwitchUserData] = FrozenList()

        for enabledUserId in enabledUserIds:
            if enabledUserId not in connectedUserIds:
                disconnectedUsers.append(enabledUsers[enabledUserId])

        disconnectedUsers.freeze()
        return disconnectedUsers

    async def __getEnabledUsers(self) -> frozendict[str, TwitchUserData]:
        allUsers = await self.__usersRepository.getUsersAsync()
        enabledUsers: dict[str, TwitchIrcReconnectHelper.TwitchUserData] = dict()

        for user in allUsers:
            if not user.isEnabled:
                continue

            try:
                userId = await self.__userIdsRepository.requireUserId(
                    userName = user.handle,
                )
            except NoSuchUserException:
                # let's just intentionally ignore this exception for now
                continue

            enabledUsers[userId] = TwitchIrcReconnectHelper.TwitchUserData(
                userId = userId,
                userName = user.handle,
            )

        return frozendict(enabledUsers)

    def setTwitchIoBot(self, twitchIoBot: Bot):
        if not isinstance(twitchIoBot, Bot):
            raise TypeError(f'twitchIoBot argument is malformed: \"{twitchIoBot}\"')

        self.__twitchIoBot = twitchIoBot

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchIrcReconnectHelper', 'Not starting TwitchIrcReconnectHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchIrcReconnectHelper', 'Starting TwitchIrcReconnectHelper...')
        self.__backgroundTaskHelper.createTask(self.__startIrcConnectionCheckRefreshLoop())

    async def __startIrcConnectionCheckRefreshLoop(self):
        # wait a bit before performing the first IRC connection check
        await asyncio.sleep(self.__sleepTimeSeconds)

        while True:
            twitchIoBot = self.__twitchIoBot

            if twitchIoBot is not None:
                try:
                    await self.__checkIrcConnections(
                        twitchIoBot = twitchIoBot,
                    )
                except Exception as e:
                    self.__timber.log('TwitchIrcReconnectHelper', f'Encountered unknown Exception when checking IRC connections', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)
