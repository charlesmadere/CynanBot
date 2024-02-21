from typing import Optional

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolder():

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backgroundTaskHelper: BackgroundTaskHelper,
        chatLogger: ChatLoggerInterface,
        cutenessUtils: Optional[CutenessUtilsInterface],
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        soundPlayerManager: Optional[SoundPlayerManagerInterface],
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface,
        triviaUtils: Optional[TriviaUtilsInterface],
        ttsManager: Optional[TtsManagerInterface],
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        twitchUtils: TwitchUtilsInterface,
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface]
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(chatLogger, ChatLoggerInterface), f"malformed {chatLogger=}"
        assert cutenessUtils is None or isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(sentMessageLogger, SentMessageLoggerInterface), f"malformed {sentMessageLogger=}"
        assert soundPlayerManager is None or isinstance(soundPlayerManager, SoundPlayerManagerInterface), f"malformed {soundPlayerManager=}"
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert triviaUtils is None or isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert ttsManager is None or isinstance(ttsManager, TtsManagerInterface), f"malformed {ttsManager=}"
        assert twitchPredictionWebsocketUtils is None or isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface), f"malformed {twitchPredictionWebsocketUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert websocketConnectionServer is None or isinstance(websocketConnectionServer, WebsocketConnectionServerInterface), f"malformed {websocketConnectionServer=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__cutenessUtils: Optional[CutenessUtilsInterface] = cutenessUtils
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__soundPlayerManager: Optional[SoundPlayerManagerInterface] = soundPlayerManager
        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaUtils: Optional[TriviaUtilsInterface] = triviaUtils
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer

    def getAdministratorProvider(self) -> AdministratorProviderInterface:
        return self.__administratorProvider

    def getBackgroundTaskHelper(self) -> BackgroundTaskHelper:
        return self.__backgroundTaskHelper

    def getChatLogger(self) -> ChatLoggerInterface:
        return self.__chatLogger

    def getCutenessUtils(self) -> Optional[CutenessUtilsInterface]:
        return self.__cutenessUtils

    def getGeneralSettingsRepository(self) -> GeneralSettingsRepository:
        return self.__generalSettingsRepository

    def getSentMessageLogger(self) -> SentMessageLoggerInterface:
        return self.__sentMessageLogger

    def getSoundPlayerManager(self) -> Optional[SoundPlayerManagerInterface]:
        return self.__soundPlayerManager

    def getStreamAlertsManager(self) -> Optional[StreamAlertsManagerInterface]:
        return self.__streamAlertsManager

    def getTimber(self) -> TimberInterface:
        return self.__timber

    def getTriviaUtils(self) -> Optional[TriviaUtilsInterface]:
        return self.__triviaUtils

    def getTtsManager(self) -> Optional[TtsManagerInterface]:
        return self.__ttsManager

    def getTwitchPredictionWebsocketUtils(self) -> Optional[TwitchPredictionWebsocketUtilsInterface]:
        return self.__twitchPredictionWebsocketUtils

    def getTwitchUtils(self) -> TwitchUtilsInterface:
        return self.__twitchUtils

    def getWebsocketConnectionServer(self) -> Optional[WebsocketConnectionServerInterface]:
        return self.__websocketConnectionServer
