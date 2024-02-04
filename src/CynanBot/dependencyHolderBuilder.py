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
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

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
        if not isinstance(instance, CutenessUtilsInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__cutenessUtils = instance
        return self

    def setSoundPlayerHelper(self, instance: SoundPlayerManagerInterface) -> Self:
        if not isinstance(instance, SoundPlayerManagerInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__soundPlayerManager = instance
        return self

    def setStreamAlertsManager(self, instance: StreamAlertsManagerInterface) -> Self:
        if not isinstance(instance, StreamAlertsManagerInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__streamAlertsManager = instance
        return self

    def setTriviaUtils(self, instance: TriviaUtilsInterface) -> Self:
        if not isinstance(instance, TriviaUtilsInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__triviaUtils = instance
        return self

    def setTtsManager(self, instance: TtsManagerInterface) -> Self:
        if not isinstance(instance, TtsManagerInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__ttsManager = instance
        return self

    def setTwitchPredictionWebsocketUtils(self, instance: TwitchPredictionWebsocketUtilsInterface) -> Self:
        if not isinstance(instance, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__twitchPredictionWebsocketUtils = instance
        return self

    def setWebsocketConnectionServer(self, instance: WebsocketConnectionServerInterface) -> Self:
        if not isinstance(instance, WebsocketConnectionServerInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__websocketConnectionServer = instance
        return self
