from typing import Optional, Self

from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.dependencyHolder import DependencyHolder
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolderBuilder():

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise ValueError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber

        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = None
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = None

    def build(self) -> DependencyHolder:
        return DependencyHolder(
            chatLogger = self.__chatLogger,
            generalSettingsRepository = self.__generalSettingsRepository,
            sentMessageLogger = self.__sentMessageLogger,
            timber = self.__timber,
            twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils,
            websocketConnectionServer = self.__websocketConnectionServer
        )

    def setTwitchPredictionWebsocketUtils(self, instance: TwitchPredictionWebsocketUtilsInterface) -> Self:
        if not isinstance(instance, TwitchPredictionWebsocketUtilsInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__twitchPredictionWebsocketUtils = instance
        return self

    def setWebsocketConnectionServer(self, instance: WebsocketConnectionServerInterface) -> Self:
        if not isinstance(instance, WebsocketConnectionServerInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__websocketConnectionServer = instance
        return self
