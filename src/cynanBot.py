import traceback
from asyncio import AbstractEventLoop
from typing import Any, Collection, Final

from frozenlist import FrozenList
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

from .chatLogger.chatLoggerInterface import ChatLoggerInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.startable import Startable
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .timber.timberInterface import TimberInterface
from .twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.websocket.listener.twitchWebsocketConnectionsFinishedListener import \
    TwitchWebsocketConnectionsFinishedListener
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface


class CynanBot(
    commands.Bot,
    TwitchWebsocketConnectionsFinishedListener,
):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatLogger: ChatLoggerInterface,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface,
        startables: Collection[Startable | Any | None] | None,
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireTwitchHandle(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15,
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise TypeError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif startables is not None and not isinstance(startables, Collection):
            raise TypeError(f'startables argument is malformed: \"{startables}\"')

        self.__authRepository: Final[AuthRepository] = authRepository
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchWebsocketClient: Final[TwitchWebsocketClientInterface] = twitchWebsocketClient
        self.__startables: Final[FrozenList[Startable]] = self.__buildStartablesCollection(startables)

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireTwitchHandle()}')

    def __buildStartablesCollection(
        self,
        startables: Collection[Startable | Any | None] | None,
    ) -> FrozenList[Startable]:
        if startables is None:
            emptyStartables: FrozenList[Startable] = FrozenList()
            emptyStartables.freeze()
            return emptyStartables

        frozenStartables: FrozenList[Startable | Any | None] = FrozenList(startables)
        frozenStartables.freeze()

        validStartables: FrozenList[Startable] = FrozenList()

        for index, startable in enumerate(frozenStartables):
            if startable is None:
                continue
            elif isinstance(startable, Startable):
                validStartables.append(startable)
            else:
                exception = TypeError(f'Encountered an invalid Startable instance ({index=}) ({startable=}) ({frozenStartables=})')
                self.__timber.log('CynanBot', f'Encountered an invalid Startable instance ({index=}) ({startable=}) ({frozenStartables=})', exception, traceback.format_exc())
                raise exception

        validStartables.freeze()
        return validStartables

    async def event_channel_join_failure(self, channel: str):
        self.__timber.log('CynanBot', f'Encountered channel join failure ({channel=})')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_ready(self):
        await self.wait_for_ready()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'Bot \"{twitchHandle}\" is ready!')

        self.__timber.start()
        self.__twitchTokensRepository.start()
        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__twitchChatMessenger.start()

        self.__twitchWebsocketClient.setConnectionsFinishedListener(self)
        self.__twitchWebsocketClient.start()

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received IRC RECONNECT event')

    async def onWebsocketConnectionsFinished(self, userIds: Collection[str]):
        self.__timber.log('CynanBot', f'Finished establishing Twitch websocket connections ({userIds=})')

        for startable in self.__startables:
            startable.start()

        self.__timber.log('CynanBot', f'Finished starting all {len(self.__startables)} startable(s)')
