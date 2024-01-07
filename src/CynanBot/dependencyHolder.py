from typing import Optional

from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolder():

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface]
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise ValueError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise ValueError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise ValueError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer

    def getChatLogger(self) -> ChatLoggerInterface:
        return self.__chatLogger

    def getGeneralSettingsRepository(self) -> GeneralSettingsRepository:
        return self.__generalSettingsRepository

    def getSentMessageLogger(self) -> SentMessageLoggerInterface:
        return self.__sentMessageLogger

    def getTimber(self) -> TimberInterface:
        return self.__timber

    def getTwitchPredictionWebsocketUtils(self) -> Optional[TwitchPredictionWebsocketUtilsInterface]:
        return self.__twitchPredictionWebsocketUtils

    def getWebsocketConnectionServer(self) -> Optional[WebsocketConnectionServerInterface]:
        return self.__websocketConnectionServer
