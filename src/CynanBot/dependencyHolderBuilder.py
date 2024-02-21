from typing import Optional, Self

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.dependencyHolder import DependencyHolder
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


class DependencyHolderBuilder():

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backgroundTaskHelper: BackgroundTaskHelper,
        chatLogger: ChatLoggerInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(chatLogger, ChatLoggerInterface), f"malformed {chatLogger=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(sentMessageLogger, SentMessageLoggerInterface), f"malformed {sentMessageLogger=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__cutenessUtils: Optional[CutenessUtilsInterface] = None
        self.__soundPlayerManager: Optional[SoundPlayerManagerInterface] = None
        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = None
        self.__triviaUtils: Optional[TriviaUtilsInterface] = None
        self.__ttsManager: Optional[TtsManagerInterface] = None
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = None
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = None

    def build(self) -> DependencyHolder:
        return DependencyHolder(
            administratorProvider = self.__administratorProvider,
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatLogger = self.__chatLogger,
            cutenessUtils = self.__cutenessUtils,
            generalSettingsRepository = self.__generalSettingsRepository,
            sentMessageLogger = self.__sentMessageLogger,
            soundPlayerManager = self.__soundPlayerManager,
            streamAlertsManager = self.__streamAlertsManager,
            timber = self.__timber,
            triviaUtils = self.__triviaUtils,
            ttsManager = self.__ttsManager,
            twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils,
            twitchUtils = self.__twitchUtils,
            websocketConnectionServer = self.__websocketConnectionServer
        )

    def setCutenessUtils(self, instance: CutenessUtilsInterface) -> Self:
        assert isinstance(instance, CutenessUtilsInterface), f"malformed {instance=}"

        self.__cutenessUtils = instance
        return self

    def setSoundPlayerHelper(self, instance: SoundPlayerManagerInterface) -> Self:
        assert isinstance(instance, SoundPlayerManagerInterface), f"malformed {instance=}"

        self.__soundPlayerManager = instance
        return self

    def setStreamAlertsManager(self, instance: StreamAlertsManagerInterface) -> Self:
        assert isinstance(instance, StreamAlertsManagerInterface), f"malformed {instance=}"

        self.__streamAlertsManager = instance
        return self

    def setTriviaUtils(self, instance: TriviaUtilsInterface) -> Self:
        assert isinstance(instance, TriviaUtilsInterface), f"malformed {instance=}"

        self.__triviaUtils = instance
        return self

    def setTtsManager(self, instance: TtsManagerInterface) -> Self:
        assert isinstance(instance, TtsManagerInterface), f"malformed {instance=}"

        self.__ttsManager = instance
        return self

    def setTwitchPredictionWebsocketUtils(self, instance: TwitchPredictionWebsocketUtilsInterface) -> Self:
        assert isinstance(instance, TwitchPredictionWebsocketUtilsInterface), f"malformed {instance=}"

        self.__twitchPredictionWebsocketUtils = instance
        return self

    def setWebsocketConnectionServer(self, instance: WebsocketConnectionServerInterface) -> Self:
        assert isinstance(instance, WebsocketConnectionServerInterface), f"malformed {instance=}"

        self.__websocketConnectionServer = instance
        return self
