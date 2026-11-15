import traceback
from typing import Any, Collection, Final

from frozenlist import FrozenList

from .chatLogger.chatLoggerInterface import ChatLoggerInterface
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.startable import Startable
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .timber.timberInterface import TimberInterface
from .twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from .twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.websocket.listener.twitchWebsocketConnectionsFinishedListener import \
    TwitchWebsocketConnectionsFinishedListener
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface


class CynanBot(Startable, TwitchWebsocketConnectionsFinishedListener):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatLogger: ChatLoggerInterface,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface,
        startables: Collection[Startable | Any | None] | None,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif startables is not None and not isinstance(startables, Collection):
            raise TypeError(f'startables argument is malformed: \"{startables}\"')

        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchWebsocketClient: Final[TwitchWebsocketClientInterface] = twitchWebsocketClient
        self.__startables: Final[FrozenList[Startable]] = self.__buildStartablesCollection(startables)

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

    async def onWebsocketConnectionsFinished(self, userIds: Collection[str]):
        self.__timber.log('CynanBot', f'Finished establishing Twitch websocket connections ({userIds=})')

        for index, startable in enumerate(self.__startables):
            try:
                startable.start()
            except Exception as e:
                self.__timber.log('CynanBot', f'Failed to start {startable} at index {index} ({userIds=}) ({self.__startables=})', e, traceback.format_exc())
                raise e

        self.__timber.log('CynanBot', f'Finished starting all {len(self.__startables)} startable(s)')

    def start(self):
        twitchHandle = self.__twitchHandleProvider.getTwitchHandle()
        self.__timber.log('CynanBot', f'Bot \"{twitchHandle}\" is starting components...')

        self.__timber.start()
        self.__twitchTokensRepository.start()
        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__twitchChatMessenger.start()

        self.__twitchWebsocketClient.setConnectionsFinishedListener(self)
        self.__twitchWebsocketClient.start()
