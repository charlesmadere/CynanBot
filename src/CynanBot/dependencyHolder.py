from typing import Optional

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolder():

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatLogger: ChatLoggerInterface,
        cutenessUtils: Optional[CutenessUtilsInterface],
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        triviaUtils: Optional[TriviaUtilsInterface],
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        twitchUtils: TwitchUtilsInterface,
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface]
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cutenessUtils is not None and not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise ValueError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaUtils is not None and not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise ValueError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise ValueError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__cutenessUtils: Optional[CutenessUtilsInterface] = cutenessUtils
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber
        self.__triviaUtils: Optional[TriviaUtilsInterface] = triviaUtils
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer

    def getAdministratorProvider(self) -> AdministratorProviderInterface:
        return self.__administratorProvider

    def getChatLogger(self) -> ChatLoggerInterface:
        return self.__chatLogger

    def getCutenessUtils(self) -> Optional[CutenessUtilsInterface]:
        return self.__cutenessUtils

    def getGeneralSettingsRepository(self) -> GeneralSettingsRepository:
        return self.__generalSettingsRepository

    def getSentMessageLogger(self) -> SentMessageLoggerInterface:
        return self.__sentMessageLogger

    def getTimber(self) -> TimberInterface:
        return self.__timber

    def getTriviaUtils(self) -> Optional[TriviaUtilsInterface]:
        return self.__triviaUtils

    def getTwitchPredictionWebsocketUtils(self) -> Optional[TwitchPredictionWebsocketUtilsInterface]:
        return self.__twitchPredictionWebsocketUtils

    def getTwitchUtils(self) -> TwitchUtilsInterface:
        return self.__twitchUtils

    def getWebsocketConnectionServer(self) -> Optional[WebsocketConnectionServerInterface]:
        return self.__websocketConnectionServer
