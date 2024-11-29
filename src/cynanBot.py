import traceback
from asyncio import AbstractEventLoop

from twitchio import Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

from .aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from .aniv.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from .aniv.anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from .aniv.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from .aniv.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from .beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from .beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from .channelPointRedemptions.absChannelPointRedemption import AbsChannelPointRedemption
from .channelPointRedemptions.casualGamePollPointRedemption import CasualGamePollPointRedemption
from .channelPointRedemptions.cutenessPointRedemption import CutenessPointRedemption
from .channelPointRedemptions.pkmnBattlePointRedemption import PkmnBattlePointRedemption
from .channelPointRedemptions.pkmnCatchPointRedemption import PkmnCatchPointRedemption
from .channelPointRedemptions.pkmnEvolvePointRedemption import PkmnEvolvePointRedemption
from .channelPointRedemptions.pkmnShinyPointRedemption import PkmnShinyPointRedemption
from .channelPointRedemptions.shizaPointRedemption import ShizaPointRedemption
from .channelPointRedemptions.soundAlertPointRedemption import SoundAlertPointRedemption
from .channelPointRedemptions.stubChannelPointRedemption import StubPointRedemption
from .channelPointRedemptions.superTriviaGamePointRedemption import SuperTriviaGamePointRedemption
from .channelPointRedemptions.timeoutPointRedemption import TimeoutPointRedemption
from .channelPointRedemptions.triviaGamePointRedemption import TriviaGamePointRedemption
from .chatActions.chatActionsManagerInterface import ChatActionsManagerInterface
from .chatCommands.absChatCommand import AbsChatCommand
from .chatCommands.addBannedTriviaControllerChatCommand import AddBannedTriviaControllerChatCommand
from .chatCommands.addCrowdControlCheerActionChatCommand import AddCrowdControlCheerActionChatCommand
from .chatCommands.addGameShuffleCheerActionChatCommand import AddGameShuffleCheerActionChatCommand
from .chatCommands.addGlobalTriviaControllerCommand import AddGlobalTriviaControllerCommand
from .chatCommands.addRecurringCutenessActionChatCommand import AddRecurringCutenessActionChatCommand
from .chatCommands.addRecurringSuperTriviaActionChatCommand import AddRecurringSuperTriviaActionChatCommand
from .chatCommands.addRecurringWeatherActionChatCommand import AddRecurringWeatherActionChatCommand
from .chatCommands.addRecurringWordOfTheDayActionChatCommand import AddRecurringWordOfTheDayActionChatCommand
from .chatCommands.addSoundAlertCheerActionCommand import AddSoundAlertCheerActionCommand
from .chatCommands.addTimeoutCheerActionCommand import AddTimeoutCheerActionCommand
from .chatCommands.addTriviaAnswerChatCommand import AddTriviaAnswerChatCommand
from .chatCommands.addTriviaControllerChatCommand import AddTriviaControllerChatCommand
from .chatCommands.anivTimeoutsChatCommand import AnivTimeoutsChatCommand
from .chatCommands.answerChatCommand import AnswerChatCommand
from .chatCommands.banTriviaQuestionChatCommand import BanTriviaQuestionChatCommand
from .chatCommands.beanInstructionsChatCommand import BeanInstructionsChatCommand
from .chatCommands.beanStatsChatCommand import BeanStatsChatCommand
from .chatCommands.clearCachesChatCommand import ClearCachesChatCommand
from .chatCommands.clearSuperTriviaQueueChatCommand import ClearSuperTriviaQueueChatCommand
from .chatCommands.commandsChatCommand import CommandsChatCommand
from .chatCommands.crowdControlChatCommand import CrowdControlChatCommand
from .chatCommands.cutenessChampionsChatCommand import CutenessChampionsChatCommand
from .chatCommands.cutenessChatCommand import CutenessChatCommand
from .chatCommands.cutenessHistoryChatCommand import CutenessHistoryChatCommand
from .chatCommands.deleteCheerActionChatCommand import DeleteCheerActionChatCommand
from .chatCommands.deleteTriviaAnswersChatCommand import DeleteTriviaAnswersChatCommand
from .chatCommands.disableCheerActionChatCommand import DisableCheerActionChatCommand
from .chatCommands.enableCheerActionChatCommand import EnableCheerActionChatCommand
from .chatCommands.getBannedTriviaControllersChatCommand import GetBannedTriviaControllersChatCommand
from .chatCommands.getCheerActionsChatCommand import GetCheerActionsChatCommand
from .chatCommands.getGlobalTriviaControllersChatCommand import GetGlobalTriviaControllersChatCommand
from .chatCommands.getRecurringActionsCommand import GetRecurringActionsCommand
from .chatCommands.getTriviaAnswersChatCommand import GetTriviaAnswersChatCommand
from .chatCommands.getTriviaControllersChatCommand import GetTriviaControllersChatCommand
from .chatCommands.giveCutenessCommand import GiveCutenessCommand
from .chatCommands.jishoChatCommand import JishoChatCommand
from .chatCommands.loremIpsumChatCommand import LoremIpsumChatCommand
from .chatCommands.myCutenessChatCommand import MyCutenessChatCommand
from .chatCommands.removeBannedTriviaControllerChatCommand import RemoveBannedTriviaControllerChatCommand
from .chatCommands.removeGlobalTriviaControllerChatCommand import RemoveGlobalTriviaControllerChatCommand
from .chatCommands.removeRecurringCutenessActionChatCommand import RemoveRecurringCutenessActionChatCommand
from .chatCommands.removeRecurringSuperTriviaActionCommand import RemoveRecurringSuperTriviaActionCommand
from .chatCommands.removeRecurringWeatherActionCommand import RemoveRecurringWeatherActionCommand
from .chatCommands.removeRecurringWordOfTheDayAction import RemoveRecurringWordOfTheDayActionCommand
from .chatCommands.removeTriviaControllerChatCommand import RemoveTriviaControllerChatCommand
from .chatCommands.stubChatCommand import StubChatCommand
from .chatCommands.superAnswerChatCommand import SuperAnswerChatCommand
from .chatCommands.superTriviaChatCommand import SuperTriviaChatCommand
from .chatCommands.testCheerActionChatCommand import TestCheerActionChatCommand
from .chatCommands.timeChatCommand import TimeChatCommand
from .chatCommands.translateChatCommand import TranslateChatCommand
from .chatCommands.triviaInfoChatCommand import TriviaInfoChatCommand
from .chatCommands.triviaScoreChatCommand import TriviaScoreChatCommand
from .chatCommands.ttsChatCommand import TtsChatCommand
from .chatCommands.unbanTriviaQuestionChatCommand import UnbanTriviaQuestionChatCommand
from .chatCommands.weatherChatCommand import WeatherChatCommand
from .chatCommands.wordChatCommand import WordChatCommand
from .chatLogger.chatLoggerInterface import ChatLoggerInterface
from .cheerActions.beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from .cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActions.cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from .cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from .commands import (AbsCommand, AddUserCommand, ConfirmCommand, CynanSourceCommand, DiscordCommand,
                       PbsCommand, PkMonCommand, PkMoveCommand, RaceCommand, SetFuntoonTokenCommand,
                       SetTwitchCodeCommand, StubCommand, SwQuoteCommand, TwitchInfoCommand,
                       TwitterCommand)
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .crowdControl.bizhawk.bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from .crowdControl.crowdControlActionHandler import CrowdControlActionHandler
from .crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from .crowdControl.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from .crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from .crowdControl.message.crowdControlMessageHandler import CrowdControlMessageHandler
from .crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from .cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from .cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from .cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from .funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from .funtoon.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from .language.jishoHelperInterface import JishoHelperInterface
from .language.languagesRepositoryInterface import LanguagesRepositoryInterface
from .language.translationHelper import TranslationHelper
from .language.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from .language.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from .location.locationsRepositoryInterface import LocationsRepositoryInterface
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc import utils as utils
from .misc.administratorProviderInterface import AdministratorProviderInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.generalSettingsRepository import GeneralSettingsRepository
from .mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from .pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from .recurringActions.cutenessRecurringEvent import CutenessRecurringEvent
from .recurringActions.recurringActionEventListener import RecurringActionEventListener
from .recurringActions.recurringActionsHelperInterface import RecurringActionsHelperInterface
from .recurringActions.recurringActionsMachineInterface import RecurringActionsMachineInterface
from .recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from .recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from .recurringActions.recurringEvent import RecurringEvent
from .recurringActions.superTriviaRecurringEvent import SuperTriviaRecurringEvent
from .recurringActions.weatherRecurringEvent import WeatherRecurringEvent
from .recurringActions.wordOfTheDayRecurringEvent import WordOfTheDayRecurringEvent
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .soundPlayerManager.immediateSoundPlayerManagerInterface import ImmediateSoundPlayerManagerInterface
from .soundPlayerManager.soundPlayerRandomizerHelper import SoundPlayerRandomizerHelperInterface
from .soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from .starWars.starWarsQuotesRepositoryInterface import StarWarsQuotesRepositoryInterface
from .storage.psqlCredentialsProviderInterface import PsqlCredentialsProviderInterface
from .streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from .streamAlertsManager.streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from .streamElements.settings.streamElementsSettingsRepositoryInterface import StreamElementsSettingsRepositoryInterface
from .streamElements.userKeyRepository.streamElementsUserKeyRepositoryInterface import \
    StreamElementsUserKeyRepositoryInterface
from .supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from .timber.timberInterface import TimberInterface
from .timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from .timeout.timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from .timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from .trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from .trivia.banned.bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from .trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from .trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from .trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from .trivia.emotes.twitch.triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from .trivia.events.absTriviaEvent import AbsTriviaEvent
from .trivia.events.clearedSuperTriviaQueueTriviaEvent import ClearedSuperTriviaQueueTriviaEvent
from .trivia.events.correctAnswerTriviaEvent import CorrectAnswerTriviaEvent
from .trivia.events.correctSuperAnswerTriviaEvent import CorrectSuperAnswerTriviaEvent
from .trivia.events.failedToFetchQuestionSuperTriviaEvent import FailedToFetchQuestionSuperTriviaEvent
from .trivia.events.failedToFetchQuestionTriviaEvent import FailedToFetchQuestionTriviaEvent
from .trivia.events.incorrectAnswerTriviaEvent import IncorrectAnswerTriviaEvent
from .trivia.events.invalidAnswerInputTriviaEvent import InvalidAnswerInputTriviaEvent
from .trivia.events.newSuperTriviaGameEvent import NewSuperTriviaGameEvent
from .trivia.events.newTriviaGameEvent import NewTriviaGameEvent
from .trivia.events.outOfTimeSuperTriviaEvent import OutOfTimeSuperTriviaEvent
from .trivia.events.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from .trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from .trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from .trivia.score.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from .trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from .trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from .trivia.triviaEventListener import TriviaEventListener
from .trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from .trivia.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from .trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import \
    OpenTriviaDatabaseSessionTokenRepositoryInterface
from .trivia.triviaRepositories.triviaRepositoryInterface import TriviaRepositoryInterface
from .trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from .trivia.triviaUtilsInterface import TriviaUtilsInterface
from .trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from .tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from .tts.ttsMonster.ttsMonsterManagerInterface import TtsMonsterManagerInterface
from .tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .ttsMonster.apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from .ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from .ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from .ttsMonster.streamerVoices.ttsMonsterStreamerVoicesRepositoryInterface import \
    TtsMonsterStreamerVoicesRepositoryInterface
from .twitch.absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from .twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from .twitch.absTwitchPollHandler import AbsTwitchPollHandler
from .twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from .twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from .twitch.configuration.absChannelJoinEvent import AbsChannelJoinEvent
from .twitch.configuration.channelJoinListener import ChannelJoinListener
from .twitch.configuration.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from .twitch.configuration.joinChannelsEvent import JoinChannelsEvent
from .twitch.configuration.twitchChannel import TwitchChannel
from .twitch.configuration.twitchChannelPointRedemptionHandler import TwitchChannelPointRedemptionHandler
from .twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from .twitch.configuration.twitchConfiguration import TwitchConfiguration
from .twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from .twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from .twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from .twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from .twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from .twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from .twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from .twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from .twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from .twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from .twitch.twitchUtilsInterface import TwitchUtilsInterface
from .twitch.twitchWebsocketDataBundleHandler import TwitchWebsocketDataBundleHandler
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from .users.addOrRemoveUserActionType import AddOrRemoveUserActionType
from .users.addOrRemoveUserData import AddOrRemoveUserData
from .users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from .users.addOrRemoveUserEventListener import AddOrRemoveUserEventListener
from .users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from .users.userInterface import UserInterface
from .users.usersRepositoryInterface import UsersRepositoryInterface
from .weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from .weather.weatherRepositoryInterface import WeatherRepositoryInterface
from .websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface


class CynanBot(
    commands.Bot,
    AddOrRemoveUserEventListener,
    ChannelJoinListener,
    RecurringActionEventListener,
    TriviaEventListener,
    TwitchChannelProvider
):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        twitchCheerHandler: AbsTwitchCheerHandler | None,
        twitchFollowHandler: AbsTwitchFollowHandler | None,
        twitchPollHandler: AbsTwitchPollHandler | None,
        twitchPredictionHandler: AbsTwitchPredictionHandler | None,
        twitchRaidHandler: AbsTwitchRaidHandler | None,
        twitchSubscriptionHandler: AbsTwitchSubscriptionHandler | None,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface | None,
        addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface,
        administratorProvider: AdministratorProviderInterface,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface | None,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface | None,
        anivSettingsRepository: AnivSettingsRepositoryInterface | None,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface | None,
        bannedWordsRepository: BannedWordsRepositoryInterface | None,
        beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None,
        beanStatsPresenter: BeanStatsPresenterInterface | None,
        beanStatsRepository: BeanStatsRepositoryInterface | None,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface | None,
        chatActionsManager: ChatActionsManagerInterface | None,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        cheerActionJsonMapper: CheerActionJsonMapperInterface | None,
        cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface | None,
        cheerActionsWizard: CheerActionsWizardInterface | None,
        crowdControlActionHandler: CrowdControlActionHandler | None,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface | None,
        crowdControlMachine: CrowdControlMachineInterface | None,
        crowdControlMessageHandler: CrowdControlMessageHandler | None,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface | None,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface | None,
        cutenessPresenter: CutenessPresenterInterface | None,
        cutenessRepository: CutenessRepositoryInterface | None,
        cutenessUtils: CutenessUtilsInterface | None,
        funtoonRepository: FuntoonRepositoryInterface | None,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface | None,
        generalSettingsRepository: GeneralSettingsRepository,
        immediateSoundPlayerManager: ImmediateSoundPlayerManagerInterface | None,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface | None,
        jishoHelper: JishoHelperInterface | None,
        languagesRepository: LanguagesRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface | None,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface | None,
        openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface | None,
        pokepediaRepository: PokepediaRepositoryInterface | None,
        psqlCredentialsProvider: PsqlCredentialsProviderInterface | None,
        recurringActionsHelper: RecurringActionsHelperInterface | None,
        recurringActionsMachine: RecurringActionsMachineInterface | None,
        recurringActionsRepository: RecurringActionsRepositoryInterface | None,
        recurringActionsWizard: RecurringActionsWizardInterface | None,
        sentMessageLogger: SentMessageLoggerInterface,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface | None,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface | None,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface | None,
        starWarsQuotesRepository: StarWarsQuotesRepositoryInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface | None,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface | None,
        streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface | None,
        supStreamerRepository: SupStreamerRepositoryInterface | None,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface | None,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface | None,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface | None,
        timeZoneRepository: TimeZoneRepositoryInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface | None,
        translationHelper: TranslationHelper | None,
        triviaBanHelper: TriviaBanHelperInterface | None,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface | None,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface | None,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface | None,
        triviaIdGenerator: TriviaIdGeneratorInterface | None,
        triviaRepository: TriviaRepositoryInterface | None,
        triviaScoreRepository: TriviaScoreRepositoryInterface | None,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface |  None,
        triviaTwitchEmoteHelper: TriviaTwitchEmoteHelperInterface | None,
        triviaUtils: TriviaUtilsInterface | None,
        trollmojiHelper: TrollmojiHelperInterface | None,
        trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface | None,
        ttsJsonMapper: TtsJsonMapperInterface | None,
        ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface | None,
        ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface | None,
        ttsMonsterManager: TtsMonsterManagerInterface | None,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface | None,
        ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface | None,
        twitchApiService: TwitchApiServiceInterface,
        twitchChannelJoinHelper: TwitchChannelJoinHelperInterface,
        twitchConfiguration: TwitchConfiguration,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface | None,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface | None,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface | None,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        weatherReportPresenter: WeatherReportPresenterInterface | None,
        weatherRepository: WeatherRepositoryInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface | None,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface | None
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireTwitchHandle(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif twitchCheerHandler is not None and not isinstance(twitchCheerHandler, AbsTwitchCheerHandler):
            raise TypeError(f'twitchCheerHandler argument is malformed: \"{twitchCheerHandler}\"')
        elif twitchFollowHandler is not None and not isinstance(twitchFollowHandler, AbsTwitchFollowHandler):
            raise TypeError(f'twitchFollowHandler argument is malformed: \"{twitchFollowHandler}\"')
        elif twitchPollHandler is not None and not isinstance(twitchPollHandler, AbsTwitchPollHandler):
            raise TypeError(f'twitchPollHandler argument is malformed: \"{twitchPollHandler}\"')
        elif twitchPredictionHandler is not None and not isinstance(twitchPredictionHandler, AbsTwitchPredictionHandler):
            raise TypeError(f'twitchPredictionHandler argument is malformed: \"{twitchPredictionHandler}\"')
        elif twitchRaidHandler is not None and not isinstance(twitchRaidHandler, AbsTwitchRaidHandler):
            raise TypeError(f'twitchRaidHandler argument is malformed: \"{twitchRaidHandler}\"')
        elif twitchSubscriptionHandler is not None and not isinstance(twitchSubscriptionHandler, AbsTwitchSubscriptionHandler):
            raise TypeError(f'twitchSubscriptionHandler argument is malformed: \"{twitchSubscriptionHandler}\"')
        elif additionalTriviaAnswersRepository is not None and not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(addOrRemoveUserDataHelper, AddOrRemoveUserDataHelperInterface):
            raise TypeError(f'addOrRemoveUserDataHelper argument is malformed: \"{addOrRemoveUserDataHelper}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif anivCopyMessageTimeoutScorePresenter is not None and not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        elif anivCopyMessageTimeoutScoreRepository is not None and not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif anivSettingsRepository is not None and not isinstance(anivSettingsRepository, AnivSettingsRepositoryInterface):
            raise TypeError(f'anivSettingsRepository argument is malformed: \"{anivSettingsRepository}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise TypeError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif bannedTriviaGameControllersRepository is not None and not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif beanChanceCheerActionHelper is not None and not isinstance(beanChanceCheerActionHelper, BeanChanceCheerActionHelperInterface):
            raise TypeError(f'beanChanceCheerActionHelper argument is malformed: \"{beanChanceCheerActionHelper}\"')
        elif beanStatsPresenter is not None and not isinstance(beanStatsPresenter, BeanStatsPresenterInterface):
            raise TypeError(f'beanStatsPresenter argument is malformed: \"{beanStatsPresenter}\"')
        elif beanStatsRepository is not None and not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif bizhawkSettingsRepository is not None and not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif chatActionsManager is not None and not isinstance(chatActionsManager, ChatActionsManagerInterface):
            raise TypeError(f'chatActionsManager argument is malformed: \"{chatActionsManager}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif cheerActionJsonMapper is not None and not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif cheerActionSettingsRepository is not None and not isinstance(cheerActionSettingsRepository, CheerActionSettingsRepositoryInterface):
            raise TypeError(f'cheerActionSettingsRepository argument is malformed: \"{cheerActionSettingsRepository}\"')
        elif cheerActionsRepository is not None and not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif cheerActionsWizard is not None and not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif crowdControlActionHandler is not None and not isinstance(crowdControlActionHandler, CrowdControlActionHandler):
            raise TypeError(f'crowdControlActionHandler argument is malformed: \"{crowdControlActionHandler}\"')
        elif crowdControlIdGenerator is not None and not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif crowdControlMachine is not None and not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif crowdControlMessageHandler is not None and not isinstance(crowdControlMessageHandler, CrowdControlMessageHandler):
            raise TypeError(f'crowdControlMessageHandler argument is malformed: \"{crowdControlMessageHandler}\"')
        elif crowdControlSettingsRepository is not None and not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif crowdControlUserInputUtils is not None and not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif cutenessPresenter is not None and not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif cutenessRepository is not None and not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is not None and not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif funtoonRepository is not None and not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise TypeError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif immediateSoundPlayerManager is not None and not isinstance(immediateSoundPlayerManager, ImmediateSoundPlayerManagerInterface):
            raise TypeError(f'immediateSoundPlayerManager argument is malformed: \"{immediateSoundPlayerManager}\"')
        elif isLiveOnTwitchRepository is not None and not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif jishoHelper is not None and not isinstance(jishoHelper, JishoHelperInterface):
            raise TypeError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif locationsRepository is not None and not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif mostRecentAnivMessageRepository is not None and not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif mostRecentAnivMessageTimeoutHelper is not None and not isinstance(mostRecentAnivMessageTimeoutHelper, MostRecentAnivMessageTimeoutHelperInterface):
            raise TypeError(f'mostRecentAnivMessageTimeoutHelper argument is malformed: \"{mostRecentAnivMessageTimeoutHelper}\"')
        elif mostRecentChatsRepository is not None and not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif openTriviaDatabaseSessionTokenRepository is not None and not isinstance(openTriviaDatabaseSessionTokenRepository, OpenTriviaDatabaseSessionTokenRepositoryInterface):
            raise TypeError(f'openTriviaDatabaseSessionTokenRepository argument is malformed: \"{openTriviaDatabaseSessionTokenRepository}\"')
        elif pokepediaRepository is not None and not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif psqlCredentialsProvider is not None and not isinstance(psqlCredentialsProvider, PsqlCredentialsProviderInterface):
            raise TypeError(f'psqlCredentialsProvider argument is malformed: \"{psqlCredentialsProvider}\"')
        elif recurringActionsHelper is not None and not isinstance(recurringActionsHelper, RecurringActionsHelperInterface):
            raise TypeError(f'recurringActionsHelper argument is malformed: \"{recurringActionsHelper}\"')
        elif recurringActionsMachine is not None and not isinstance(recurringActionsMachine, RecurringActionsMachineInterface):
            raise TypeError(f'recurringActionsMachine argument is malformed: \"{recurringActionsMachine}\"')
        elif recurringActionsRepository is not None and not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif recurringActionsWizard is not None and not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif shinyTriviaOccurencesRepository is not None and not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface):
            raise TypeError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif soundPlayerRandomizerHelper is not None and not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif soundPlayerSettingsRepository is not None and not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif starWarsQuotesRepository is not None and not isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface):
            raise TypeError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif streamAlertsSettingsRepository is not None and not isinstance(streamAlertsSettingsRepository, StreamAlertsSettingsRepositoryInterface):
            raise TypeError(f'streamAlertsSettingsRepository argument is malformed: \"{streamAlertsSettingsRepository}\"')
        elif streamElementsSettingsRepository is not None and not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif streamElementsUserKeyRepository is not None and not isinstance(streamElementsUserKeyRepository, StreamElementsUserKeyRepositoryInterface):
            raise TypeError(f'streamElementsUserKeyRepository argument is malformed: \"{streamElementsUserKeyRepository}\"')
        elif supStreamerRepository is not None and not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutActionHelper is not None and not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif timeoutActionHistoryRepository is not None and not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif timeoutActionSettingsRepository is not None and not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif toxicTriviaOccurencesRepository is not None and not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif translationHelper is not None and not isinstance(translationHelper, TranslationHelper):
            raise TypeError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif triviaBanHelper is not None and not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise TypeError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif triviaEmoteGenerator is not None and not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameControllersRepository is not None and not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif triviaGameGlobalControllersRepository is not None and not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif triviaHistoryRepository is not None and not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif triviaIdGenerator is not None and not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif triviaRepository is not None and not isinstance(triviaRepository, TriviaRepositoryInterface):
            raise TypeError(f'triviaRepository argument is malformed: \"{triviaRepository}\"')
        elif triviaScoreRepository is not None and not isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface):
            raise TypeError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif triviaSettingsRepository is not None and not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif triviaTwitchEmoteHelper is not None and not isinstance(triviaTwitchEmoteHelper, TriviaTwitchEmoteHelperInterface):
            raise TypeError(f'triviaTwitchEmoteHelper argument is malformed: \"{triviaTwitchEmoteHelper}\"')
        elif triviaUtils is not None and not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif trollmojiHelper is not None and not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif trollmojiSettingsRepository is not None and not isinstance(trollmojiSettingsRepository, TrollmojiSettingsRepositoryInterface):
            raise TypeError(f'trollmojiSettingsRepository argument is malformed: \"{trollmojiSettingsRepository}\"')
        elif ttsJsonMapper is not None and not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif ttsMonsterApiTokensRepository is not None and not isinstance(ttsMonsterApiTokensRepository, TtsMonsterApiTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterApiTokensRepository argument is malformed: \"{ttsMonsterApiTokensRepository}\"')
        elif ttsMonsterKeyAndUserIdRepository is not None and not isinstance(ttsMonsterKeyAndUserIdRepository, TtsMonsterKeyAndUserIdRepositoryInterface):
            raise TypeError(f'ttsMonsterKeyAndUserIdRepository argument is malformed: \"{ttsMonsterKeyAndUserIdRepository}\"')
        elif ttsMonsterManager is not None and not isinstance(ttsMonsterManager, TtsMonsterManagerInterface):
            raise TypeError(f'ttsMonsterManager argument is malformed: \"{ttsMonsterManager}\"')
        elif ttsMonsterSettingsRepository is not None and not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif ttsMonsterStreamerVoicesRepository is not None and not isinstance(ttsMonsterStreamerVoicesRepository, TtsMonsterStreamerVoicesRepositoryInterface):
            raise TypeError(f'ttsMonsterStreamerVoicesRepository argument is malformed: \"{ttsMonsterStreamerVoicesRepository}\"')
        elif ttsSettingsRepository is not None and not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchChannelJoinHelper, TwitchChannelJoinHelperInterface):
            raise TypeError(f'twitchChannelJoinHelper argument is malformed: \"{twitchChannelJoinHelper}\"')
        elif not isinstance(twitchConfiguration, TwitchConfiguration):
            raise TypeError(f'twitchConfiguration argument is malformed: \"{twitchConfiguration}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif twitchFriendsUserIdRepository is not None and not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif twitchMessageStringUtils is not None and not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif twitchTimeoutHelper is not None and not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif twitchTimeoutRemodHelper is not None and not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif twitchWebsocketClient is not None and not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherReportPresenter is not None and not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif weatherRepository is not None and not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif wordOfTheDayPresenter is not None and not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')
        elif wordOfTheDayRepository is not None and not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__twitchCheerHandler: AbsTwitchCheerHandler | None = twitchCheerHandler
        self.__twitchFollowHandler: AbsTwitchFollowHandler | None = twitchFollowHandler
        self.__twitchPollHandler: AbsTwitchPollHandler | None = twitchPollHandler
        self.__twitchPredictionHandler: AbsTwitchPredictionHandler | None = twitchPredictionHandler
        self.__twitchRaidHandler: AbsTwitchRaidHandler | None = twitchRaidHandler
        self.__twitchSubscriptionHandler: AbsTwitchSubscriptionHandler | None = twitchSubscriptionHandler
        self.__addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface = addOrRemoveUserDataHelper
        self.__authRepository: AuthRepository = authRepository
        self.__beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None = beanChanceCheerActionHelper
        self.__chatActionsManager: ChatActionsManagerInterface | None = chatActionsManager
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__crowdControlActionHandler: CrowdControlActionHandler | None = crowdControlActionHandler
        self.__crowdControlMachine: CrowdControlMachineInterface | None = crowdControlMachine
        self.__crowdControlMessageHandler: CrowdControlMessageHandler | None = crowdControlMessageHandler
        self.__cutenessPresenter: CutenessPresenterInterface | None = cutenessPresenter
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = mostRecentAnivMessageTimeoutHelper
        self.__recurringActionsMachine: RecurringActionsMachineInterface | None = recurringActionsMachine
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface | None = timeoutActionHelper
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine
        self.__triviaRepository: TriviaRepositoryInterface | None = triviaRepository
        self.__triviaUtils: TriviaUtilsInterface | None = triviaUtils
        self.__ttsMonsterManager: TtsMonsterManagerInterface | None = ttsMonsterManager
        self.__twitchChannelJoinHelper: TwitchChannelJoinHelperInterface = twitchChannelJoinHelper
        self.__twitchConfiguration: TwitchConfiguration = twitchConfiguration
        self.__twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None = twitchTimeoutRemodHelper
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__twitchWebsocketClient: TwitchWebsocketClientInterface | None = twitchWebsocketClient
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__weatherReportPresenter: WeatherReportPresenterInterface | None = weatherReportPresenter
        self.__websocketConnectionServer: WebsocketConnectionServerInterface | None = websocketConnectionServer
        self.__wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None = wordOfTheDayPresenter

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__addUserCommand: AbsCommand = AddUserCommand(addOrRemoveUserDataHelper, administratorProvider, timber, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository)
        self.__clearCachesCommand: AbsChatCommand = ClearCachesChatCommand(addOrRemoveUserDataHelper, administratorProvider, anivSettingsRepository, authRepository, bannedWordsRepository, bizhawkSettingsRepository, cheerActionSettingsRepository, cheerActionsRepository, crowdControlSettingsRepository, funtoonTokensRepository, generalSettingsRepository, isLiveOnTwitchRepository, locationsRepository, mostRecentAnivMessageRepository, mostRecentChatsRepository, openTriviaDatabaseSessionTokenRepository, psqlCredentialsProvider, soundPlayerRandomizerHelper, soundPlayerSettingsRepository, streamAlertsSettingsRepository, streamElementsSettingsRepository, streamElementsUserKeyRepository, supStreamerRepository, timber, timeoutActionHistoryRepository, timeoutActionSettingsRepository, triviaSettingsRepository, trollmojiHelper, trollmojiSettingsRepository, ttsMonsterApiTokensRepository, ttsMonsterKeyAndUserIdRepository, ttsMonsterSettingsRepository, ttsMonsterStreamerVoicesRepository, ttsSettingsRepository, twitchEmotesHelper, twitchFollowingStatusRepository, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository, weatherRepository, wordOfTheDayRepository)
        self.__commandsCommand: AbsChatCommand = CommandsChatCommand(timber, twitchUtils, usersRepository)
        self.__confirmCommand: AbsCommand = ConfirmCommand(addOrRemoveUserDataHelper, administratorProvider, timber, twitchUtils, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(timber, twitchUtils, usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(timber, twitchUtils, usersRepository)
        self.__loremIpsumCommand: AbsChatCommand = LoremIpsumChatCommand(administratorProvider, timber, twitchUtils, usersRepository)
        self.__mastodonCommand: AbsCommand = StubCommand()
        self.__pbsCommand: AbsCommand = PbsCommand(timber, twitchUtils, usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(timber, twitchUtils, usersRepository)
        self.__setTwitchCodeCommand: AbsCommand = SetTwitchCodeCommand(administratorProvider, timber, twitchTokensRepository, twitchUtils, usersRepository)
        self.__timeCommand: AbsChatCommand = TimeChatCommand(timber, twitchUtils, usersRepository)
        self.__twitchInfoCommand: AbsCommand = TwitchInfoCommand(administratorProvider, timber, twitchApiService, authRepository, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(timber, twitchUtils, usersRepository)

        if beanStatsPresenter is None or beanStatsRepository is None:
            self.__beanStatsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__beanStatsCommand: AbsChatCommand = BeanStatsChatCommand(beanStatsPresenter, beanStatsRepository, timber, twitchUtils, usersRepository)

        if cheerActionJsonMapper is None or cheerActionsRepository is None or cheerActionsWizard is None:
            self.__addCrowdControlCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addGameShuffleCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addSoundAlertCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addTimeoutCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__beanInstructionsCommand: AbsChatCommand = StubChatCommand()
            self.__deleteCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__disableCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__enableCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__getCheerActionsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addCrowdControlCheerActionCommand: AbsChatCommand = AddCrowdControlCheerActionChatCommand(administratorProvider, cheerActionsWizard, timber, twitchUtils, usersRepository)
            self.__addGameShuffleCheerActionCommand: AbsChatCommand = AddGameShuffleCheerActionChatCommand(administratorProvider, cheerActionsWizard, timber, twitchUtils, usersRepository)
            self.__addSoundAlertCheerActionCommand: AbsChatCommand = AddSoundAlertCheerActionCommand(administratorProvider, cheerActionsWizard, timber, twitchUtils, usersRepository)
            self.__addTimeoutCheerActionCommand: AbsChatCommand = AddTimeoutCheerActionCommand(administratorProvider, cheerActionsWizard, timber, twitchUtils, usersRepository)
            self.__beanInstructionsCommand: AbsChatCommand = BeanInstructionsChatCommand(cheerActionsRepository, timber, twitchUtils, usersRepository)
            self.__deleteCheerActionCommand: AbsChatCommand = DeleteCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__disableCheerActionCommand: AbsChatCommand = DisableCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, usersRepository)
            self.__enableCheerActionCommand: AbsChatCommand = EnableCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, usersRepository)
            self.__getCheerActionsCommand: AbsChatCommand = GetCheerActionsChatCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, userIdsRepository, usersRepository)

        if crowdControlIdGenerator is None or crowdControlMachine is None or crowdControlUserInputUtils is None:
            self.__crowdControlCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__crowdControlCommand: AbsChatCommand = CrowdControlChatCommand(administratorProvider, crowdControlIdGenerator, crowdControlMachine, crowdControlUserInputUtils, timber, timeZoneRepository, twitchUtils, usersRepository)

        if recurringActionsHelper is None or recurringActionsMachine is None or recurringActionsRepository is None or recurringActionsWizard is None:
            self.__addRecurringCutenessActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringSuperTriviaActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringWeatherActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringWordOfTheDayActionCommand: AbsChatCommand = StubChatCommand()
            self.__recurringActionsCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringCutenessActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringSuperTriviaActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringWeatherActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringWordOfTheDayActionCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addRecurringCutenessActionCommand: AbsChatCommand = AddRecurringCutenessActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchUtils, usersRepository)
            self.__addRecurringSuperTriviaActionCommand: AbsChatCommand = AddRecurringSuperTriviaActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchUtils, usersRepository)
            self.__addRecurringWeatherActionCommand: AbsChatCommand = AddRecurringWeatherActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchUtils, usersRepository)
            self.__addRecurringWordOfTheDayActionCommand: AbsChatCommand = AddRecurringWordOfTheDayActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchUtils, usersRepository)
            self.__recurringActionsCommand: AbsChatCommand = GetRecurringActionsCommand(administratorProvider, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringCutenessActionCommand: AbsChatCommand = RemoveRecurringCutenessActionChatCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringSuperTriviaActionCommand: AbsChatCommand = RemoveRecurringSuperTriviaActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringWeatherActionCommand: AbsChatCommand = RemoveRecurringWeatherActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringWordOfTheDayActionCommand: AbsChatCommand = RemoveRecurringWordOfTheDayActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)

        if bannedTriviaGameControllersRepository is None or triviaUtils is None:
            self.__addBannedTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__getBannedTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__removeBannedTriviaControllerCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addBannedTriviaControllerCommand: AbsChatCommand = AddBannedTriviaControllerChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)
            self.__getBannedTriviaControllersCommand: AbsChatCommand = GetBannedTriviaControllersChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, triviaUtils, twitchUtils, usersRepository)
            self.__removeBannedTriviaControllerCommand: AbsChatCommand = RemoveBannedTriviaControllerChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or cutenessUtils is None or shinyTriviaOccurencesRepository is None or toxicTriviaOccurencesRepository is None or triviaBanHelper is None or triviaEmoteGenerator is None or triviaGameBuilder is None or triviaGameControllersRepository is None or triviaGameGlobalControllersRepository is None or triviaGameMachine is None or triviaHistoryRepository is None or triviaIdGenerator is None or triviaScoreRepository is None or triviaSettingsRepository is None or triviaUtils is None:
            self.__addGlobalTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__addTriviaAnswerCommand: AbsChatCommand = StubChatCommand()
            self.__addTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__answerCommand: AbsChatCommand = StubChatCommand()
            self.__banTriviaQuestionCommand: AbsChatCommand = StubChatCommand()
            self.__clearSuperTriviaQueueCommand: AbsChatCommand = StubChatCommand()
            self.__deleteTriviaAnswersCommand: AbsChatCommand = StubChatCommand()
            self.__getGlobalTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__getTriviaAnswersCommand: AbsChatCommand = StubChatCommand()
            self.__getTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__removeTriviaControllerChatCommand: AbsChatCommand = StubChatCommand()
            self.__superAnswerCommand: AbsChatCommand = StubChatCommand()
            self.__superTriviaCommand: AbsChatCommand = StubChatCommand()
            self.__triviaInfoCommand: AbsChatCommand = StubChatCommand()
            self.__triviaScoreCommand: AbsChatCommand = StubChatCommand()
            self.__removeGlobalTriviaControllerChatCommand: AbsChatCommand = StubChatCommand()
            self.__unbanTriviaQuestionChatCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addGlobalTriviaControllerCommand: AbsChatCommand = AddGlobalTriviaControllerCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)
            self.__addTriviaControllerCommand: AbsChatCommand = AddTriviaControllerChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)
            self.__addTriviaAnswerCommand: AbsChatCommand = AddTriviaAnswerChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__answerCommand: AbsChatCommand = AnswerChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__banTriviaQuestionCommand: AbsChatCommand = BanTriviaQuestionChatCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__clearSuperTriviaQueueCommand: AbsChatCommand = ClearSuperTriviaQueueChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, triviaUtils, usersRepository)
            self.__deleteTriviaAnswersCommand: AbsChatCommand = DeleteTriviaAnswersChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__getGlobalTriviaControllersCommand: AbsChatCommand = GetGlobalTriviaControllersChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameGlobalControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__getTriviaAnswersCommand: AbsChatCommand = GetTriviaAnswersChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__getTriviaControllersCommand: AbsChatCommand = GetTriviaControllersChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeGlobalTriviaControllerChatCommand: AbsChatCommand = RemoveGlobalTriviaControllerChatCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)
            self.__removeTriviaControllerChatCommand: AbsChatCommand = RemoveTriviaControllerChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)
            self.__superAnswerCommand: AbsChatCommand = SuperAnswerChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__superTriviaCommand: AbsChatCommand = SuperTriviaChatCommand(generalSettingsRepository, timber, triviaGameBuilder, triviaGameMachine, triviaSettingsRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaInfoCommand: AbsChatCommand = TriviaInfoChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaScoreCommand: AbsChatCommand = TriviaScoreChatCommand(generalSettingsRepository, shinyTriviaOccurencesRepository, timber, toxicTriviaOccurencesRepository, triviaScoreRepository, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__unbanTriviaQuestionChatCommand: AbsChatCommand = UnbanTriviaQuestionChatCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)

        if cutenessPresenter is None or cutenessRepository is None or cutenessUtils is None or triviaUtils is None:
            self.__cutenessCommand: AbsChatCommand = StubChatCommand()
            self.__cutenessChampionsCommand: AbsChatCommand = StubChatCommand()
            self.__cutenessHistoryCommand: AbsChatCommand = StubChatCommand()
            self.__giveCutenessCommand: AbsChatCommand = StubChatCommand()
            self.__myCutenessCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__cutenessCommand: AbsChatCommand = CutenessChatCommand(cutenessPresenter, cutenessRepository, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsChatCommand = CutenessChampionsChatCommand(cutenessPresenter, cutenessRepository, timber, twitchUtils, usersRepository)
            self.__cutenessHistoryCommand: AbsChatCommand = CutenessHistoryChatCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsChatCommand = GiveCutenessCommand(cutenessRepository, timber, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsChatCommand = MyCutenessChatCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, usersRepository)

        if funtoonTokensRepository is None:
            self.__setFuntoonTokenCommand: AbsCommand = StubCommand()
        else:
            self.__setFuntoonTokenCommand: AbsCommand = SetFuntoonTokenCommand(administratorProvider, funtoonTokensRepository, timber, twitchUtils, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__jishoCommand: AbsChatCommand = JishoChatCommand(generalSettingsRepository, jishoHelper, timber, twitchUtils, usersRepository)

        if anivCopyMessageTimeoutScorePresenter is None or anivCopyMessageTimeoutScoreRepository is None:
            self.__anivTimeoutsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__anivTimeoutsCommand: AbsChatCommand = AnivTimeoutsChatCommand(anivCopyMessageTimeoutScorePresenter, anivCopyMessageTimeoutScoreRepository, timber, twitchUtils, userIdsRepository, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsCommand = StubCommand()
            self.__pkMoveCommand: AbsCommand = StubCommand()
        else:
            self.__pkMonCommand: AbsCommand = PkMonCommand(generalSettingsRepository, pokepediaRepository, timber, twitchUtils, usersRepository)
            self.__pkMoveCommand: AbsCommand = PkMoveCommand(generalSettingsRepository, pokepediaRepository, timber, twitchUtils, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsCommand = StubCommand()
        else:
            self.__swQuoteCommand: AbsCommand = SwQuoteCommand(starWarsQuotesRepository, timber, twitchUtils, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__translateCommand: AbsChatCommand = TranslateChatCommand(generalSettingsRepository, languagesRepository, timber, translationHelper, twitchUtils, usersRepository)

        if streamAlertsManager is None or ttsJsonMapper is None:
            self.__ttsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__ttsCommand: AbsChatCommand = TtsChatCommand(administratorProvider, streamAlertsManager, timber, ttsJsonMapper, twitchUtils, usersRepository)

        if locationsRepository is None or weatherReportPresenter is None or weatherRepository is None:
            self.__weatherCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__weatherCommand: AbsChatCommand = WeatherChatCommand(locationsRepository, timber, twitchUtils, usersRepository, weatherReportPresenter, weatherRepository)

        if cheerActionHelper is None:
            self.__testCheerActionCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__testCheerActionCommand: AbsChatCommand = TestCheerActionChatCommand(cheerActionHelper, timber, twitchUtils, usersRepository)

        if wordOfTheDayPresenter is None or wordOfTheDayRepository is None:
            self.__wordCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__wordCommand: AbsChatCommand = WordChatCommand(languagesRepository, timber, twitchUtils, usersRepository, wordOfTheDayPresenter, wordOfTheDayRepository)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        self.__casualGamePollPointRedemption: AbsChannelPointRedemption = CasualGamePollPointRedemption(timber, twitchUtils)
        self.__shizaPointRedemption: AbsChannelPointRedemption = ShizaPointRedemption(timber, twitchUtils)

        if cutenessRepository is None:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = CutenessPointRedemption(cutenessRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = PkmnBattlePointRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = PkmnCatchPointRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = PkmnEvolvePointRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = PkmnShinyPointRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if immediateSoundPlayerManager is None or soundPlayerRandomizerHelper is None or streamAlertsManager is None:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = SoundAlertPointRedemption(immediateSoundPlayerManager, soundPlayerRandomizerHelper, streamAlertsManager)

        if timeoutActionHelper is None:
            self.__timeoutPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__timeoutPointRedemption: AbsChannelPointRedemption = TimeoutPointRedemption(timber, timeoutActionHelper, authRepository, twitchMessageStringUtils, twitchTokensRepository, twitchUtils, userIdsRepository)

        if cutenessRepository is None or triviaGameBuilder is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = SuperTriviaGamePointRedemption(timber, triviaGameBuilder, triviaGameMachine)
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = TriviaGamePointRedemption(timber, triviaGameBuilder, triviaGameMachine)

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireTwitchHandle()}')

    async def event_channel_join_failure(self, channel: str):
        userId = await self.__userIdsRepository.fetchUserId(channel)
        user: UserInterface | None = None
        exception: Exception | None = None

        try:
            user = await self.__usersRepository.getUserAsync(channel)
        except Exception as e:
            exception = e

        if user is None or exception is not None:
            self.__timber.log('CynanBot', f'Failed to join channel, and also failed to retrieve a user for this channel ({channel=}) ({userId=}) ({user=}): {exception}', exception, traceback.format_exc())
            return

        self.__timber.log('CynanBot', f'Failed to join channel ({channel=}) ({userId=}) ({user=}), disabling this user...')

        await self.__usersRepository.setUserEnabled(
            handle = user.getHandle(),
            enabled = False
        )

        self.__timber.log('CynanBot', f'Finished disabling user due to channel join failure ({channel=}) ({userId=}) ({user=})')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        twitchMessage = self.__twitchConfiguration.getMessage(message)

        if await twitchMessage.isMessageFromExternalSharedChat():
            return

        if self.__chatActionsManager is not None:
            await self.__chatActionsManager.handleMessage(twitchMessage)

        await self.handle_commands(message)

    async def event_ready(self):
        await self.wait_for_ready()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'{twitchHandle} is ready!')

        self.__twitchChannelJoinHelper.setChannelJoinListener(self)
        self.__twitchChannelJoinHelper.joinChannels()

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received new reconnect event')
        await self.wait_for_ready()
        self.__timber.log('CynanBot', f'Finished reconnecting')

    async def event_usernotice_subscription(self, metadata):
        self.__timber.log('CynanBot', f'event_usernotice_subscription(): (metadata=\"{metadata}\")')

    async def __getChannel(self, twitchChannel: str) -> TwitchChannel:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.wait_for_ready()

        try:
            channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBot', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return self.__twitchConfiguration.getChannel(channel)
        except KeyError as e:
            self.__timber.log('CynanBot', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())

    async def getTwitchChannel(self, twitchChannel: str) -> TwitchChannel:
        return await self.__getChannel(twitchChannel)

    async def onAddOrRemoveUserEvent(self, event: AddOrRemoveUserData):
        self.__timber.log('CynanBot', f'Received new modify user data event: {event}')

        await self.wait_for_ready()

        match event.actionType:
            case AddOrRemoveUserActionType.ADD:
                channels: list[str] = list()
                channels.append(event.userName)
                await self.join_channels(channels)

            case AddOrRemoveUserActionType.REMOVE:
                channels: list[str] = list()
                channels.append(event.userName)
                await self.part_channels(channels)

            case _:
                raise RuntimeError(f'unknown AddOrRemoveUserActionType: \"{event.actionType}\"')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        eventType = event.getEventType()
        self.__timber.log('CynanBot', f'Received new channel join event: \"{eventType}\"')

        await self.wait_for_ready()

        if isinstance(event, FinishedJoiningChannelsEvent):
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif isinstance(event, JoinChannelsEvent):
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBot', f'Finished joining channels: {event.getAllChannels()}')

        self.__addOrRemoveUserDataHelper.setAddOrRemoveUserEventListener(self)
        self.__timber.start()
        self.__twitchTokensRepository.start()
        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__streamAlertsManager.start()
        self.__twitchUtils.start()

        if self.__beanChanceCheerActionHelper is not None:
            self.__beanChanceCheerActionHelper.setTwitchChannelProvider(self)

        if self.__crowdControlActionHandler is not None:
            self.__crowdControlActionHandler.start()

        if self.__crowdControlMachine is not None:
            self.__crowdControlMachine.setActionHandler(self.__crowdControlActionHandler)

            if self.__crowdControlMessageHandler is not None:
                self.__crowdControlMessageHandler.setTwitchChannelProvider(self)
                self.__crowdControlMachine.setMessageListener(self.__crowdControlMessageHandler)

            self.__crowdControlMachine.start()

        if self.__timeoutActionHelper is not None:
            self.__timeoutActionHelper.setTwitchChannelProvider(self)

        if self.__mostRecentAnivMessageTimeoutHelper is not None:
            self.__mostRecentAnivMessageTimeoutHelper.setTwitchChannelProvider(self)

        if self.__twitchTimeoutRemodHelper is not None:
            self.__twitchTimeoutRemodHelper.start()

        if self.__triviaRepository is not None:
            self.__triviaRepository.startSpooler()

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self)
            self.__triviaGameMachine.startMachine()

        if self.__ttsMonsterManager is not None:
            self.__ttsMonsterManager.setTwitchChannelProvider(self)

        if self.__recurringActionsMachine is not None:
            self.__recurringActionsMachine.setEventListener(self)
            self.__recurringActionsMachine.startMachine()

        if self.__websocketConnectionServer is not None:
            self.__websocketConnectionServer.start()

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isEventSubEnabled() and self.__twitchWebsocketClient is not None:
            channelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None = TwitchChannelPointRedemptionHandler(
                casualGamePollPointRedemption = self.__casualGamePollPointRedemption,
                cutenessPointRedemption = self.__cutenessPointRedemption,
                pkmnBattlePointRedemption = self.__pkmnBattlePointRedemption,
                pkmnCatchPointRedemption = self.__pkmnCatchPointRedemption,
                pkmnEvolvePointRedemption = self.__pkmnEvolvePointRedemption,
                pkmnShinyPointRedemption = self.__pkmnShinyPointRedemption,
                shizaPointRedemption = self.__shizaPointRedemption,
                soundAlertPointRedemption = self.__soundAlertPointRedemption,
                superTriviaGamePointRedemption = self.__superTriviaGamePointRedemption,
                timeoutPointRedemption = self.__timeoutPointRedemption,
                triviaGamePointRedemption = self.__triviaGamePointRedemption,
                timber = self.__timber,
                userIdsRepository = self.__userIdsRepository
            )

            channelPointRedemptionHandler.setTwitchChannelProvider(self)

            if self.__twitchCheerHandler is not None:
                self.__twitchCheerHandler.setTwitchChannelProvider(self)

            if self.__twitchFollowHandler is not None:
                self.__twitchFollowHandler.setTwitchChannelProvider(self)

            if self.__twitchPollHandler is not None:
                self.__twitchPollHandler.setTwitchChannelProvider(self)

            if self.__twitchPredictionHandler is not None:
                self.__twitchPredictionHandler.setTwitchChannelProvider(self)

            if self.__twitchRaidHandler is not None:
                self.__twitchRaidHandler.setTwitchChannelProvider(self)

            if self.__twitchSubscriptionHandler is not None:
                self.__twitchSubscriptionHandler.setTwitchChannelProvider(self)
                self.__twitchSubscriptionHandler.start()

            self.__twitchWebsocketClient.setDataBundleListener(TwitchWebsocketDataBundleHandler(
                channelPointRedemptionHandler = channelPointRedemptionHandler,
                cheerHandler = self.__twitchCheerHandler,
                followHandler = self.__twitchFollowHandler,
                pollHandler = self.__twitchPollHandler,
                predictionHandler = self.__twitchPredictionHandler,
                raidHandler = self.__twitchRaidHandler,
                subscriptionHandler = self.__twitchSubscriptionHandler,
                timber = self.__timber,
                userIdsRepository = self.__userIdsRepository,
                usersRepository = self.__usersRepository
            ))

            self.__twitchWebsocketClient.start()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event.getChannels()}')
        await self.join_channels(event.getChannels())

    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        await self.wait_for_ready()

        self.__timber.log('CynanBot', f'Received new recurring action event: \"{event}\"')

        if isinstance(event, CutenessRecurringEvent):
            await self.__handleCutenessRecurringActionEvent(event)
        elif isinstance(event, SuperTriviaRecurringEvent):
            await self.__handleSuperTriviaRecurringActionEvent(event)
        elif isinstance(event, WeatherRecurringEvent):
            await self.__handleWeatherRecurringActionEvent(event)
        elif isinstance(event, WordOfTheDayRecurringEvent):
            await self.__handleWordOfTheDayRecurringActionEvent(event)

    async def __handleCutenessRecurringActionEvent(self, event: CutenessRecurringEvent):
        if not isinstance(event, CutenessRecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        cutenessPresenter = self.__cutenessPresenter

        if cutenessPresenter is None:
            return

        twitchChannel = await self.__getChannel(event.twitchChannel)
        leaderboardString = await cutenessPresenter.printLeaderboard(event.leaderboard)
        await self.__twitchUtils.safeSend(twitchChannel, leaderboardString)

    async def __handleSuperTriviaRecurringActionEvent(self, event: SuperTriviaRecurringEvent):
        if not isinstance(event, SuperTriviaRecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        twitchChannel = await self.__getChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, 'Super trivia starting soon!')

    async def __handleWeatherRecurringActionEvent(self, event: WeatherRecurringEvent):
        if not isinstance(event, WeatherRecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        weatherReportPresenter = self.__weatherReportPresenter

        if weatherReportPresenter is None:
            return

        twitchChannel = await self.__getChannel(event.twitchChannel)
        weatherReportString = await weatherReportPresenter.toString(event.weatherReport)
        await self.__twitchUtils.safeSend(twitchChannel, weatherReportString)

    async def __handleWordOfTheDayRecurringActionEvent(self, event: WordOfTheDayRecurringEvent):
        if not isinstance(event, WordOfTheDayRecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        wordOfTheDayPresenter = self.__wordOfTheDayPresenter

        if wordOfTheDayPresenter is None:
            return

        twitchChannel = await self.__getChannel(event.twitchChannel)

        wordOfTheDayString = await wordOfTheDayPresenter.toString(
            includeRomaji = False,
            wordOfTheDay = event.wordOfTheDayResponse
        )

        await self.__twitchUtils.safeSend(twitchChannel, wordOfTheDayString)

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        await self.wait_for_ready()

        self.__timber.log('CynanBot', f'Received new trivia event: \"{event}\"')

        if isinstance(event, ClearedSuperTriviaQueueTriviaEvent):
            await self.__handleClearedSuperTriviaQueueTriviaEvent(event)
        elif isinstance(event, CorrectAnswerTriviaEvent):
            await self.__handleCorrectAnswerTriviaEvent(event)
        elif isinstance(event, FailedToFetchQuestionTriviaEvent):
            await self.__handleFailedToFetchQuestionTriviaEvent(event)
        elif isinstance(event, OutOfTimeTriviaEvent):
            await self.__handleGameOutOfTimeTriviaEvent(event)
        elif isinstance(event, IncorrectAnswerTriviaEvent):
            await self.__handleIncorrectAnswerTriviaEvent(event)
        elif isinstance(event, InvalidAnswerInputTriviaEvent):
            await self.__handleInvalidAnswerInputTriviaEvent(event)
        elif isinstance(event, NewTriviaGameEvent):
            await self.__handleNewTriviaGameEvent(event)
        elif isinstance(event, NewSuperTriviaGameEvent):
            await self.__handleNewSuperTriviaGameEvent(event)
        elif isinstance(event, FailedToFetchQuestionSuperTriviaEvent):
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(event)
        elif isinstance(event, CorrectSuperAnswerTriviaEvent):
            await self.__handleSuperGameCorrectAnswerTriviaEvent(event)
        elif isinstance(event, OutOfTimeSuperTriviaEvent):
            await self.__handleSuperGameOutOfTimeTriviaEvent(event)

    async def __handleClearedSuperTriviaQueueTriviaEvent(self, event: ClearedSuperTriviaQueueTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        message = await self.__triviaUtils.getClearedSuperTriviaQueueMessage(
            numberOfGamesRemoved = event.numberOfGamesRemoved
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleCorrectAnswerTriviaEvent(self, event: CorrectAnswerTriviaEvent):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        message = await self.__triviaUtils.getCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        )

        twitchChannel = await self.__getChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleFailedToFetchQuestionTriviaEvent(self, event: FailedToFetchQuestionTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(self, event: FailedToFetchQuestionSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameOutOfTimeTriviaEvent(self, event: OutOfTimeTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            outOfTimeEmote = event.outOfTimeEmote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleIncorrectAnswerTriviaEvent(self, event: IncorrectAnswerTriviaEvent):
        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        message = await self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            wrongAnswerEmote = event.wrongAnswerEmote,
            specialTriviaStatus = event.specialTriviaStatus
        )

        twitchChannel = await self.__getChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleInvalidAnswerInputTriviaEvent(self, event: InvalidAnswerInputTriviaEvent):
        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        message = await self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus
        )

        twitchChannel = await self.__getChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleNewTriviaGameEvent(self, event: NewTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleNewSuperTriviaGameEvent(self, event: NewSuperTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleSuperGameCorrectAnswerTriviaEvent(self, event: CorrectSuperAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        message = await self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            points = event.pointsForWinning,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userName = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleSuperGameOutOfTimeTriviaEvent(self, event: OutOfTimeSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        if not isinstance(self.__triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{self.__triviaUtils}\"')

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            outOfTimeEmote = event.outOfTimeEmote,
            specialTriviaStatus = event.specialTriviaStatus
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    @commands.command(name = 'addbannedtriviacontroller')
    async def command_addbannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addBannedTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'addcrowdcontrolaction')
    async def command_addcrowdcontrolaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addCrowdControlCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addgameshuffleaction')
    async def command_addgameshuffleaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGameShuffleCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addglobaltriviacontroller')
    async def command_addglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGlobalTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringcutenessaction')
    async def command_addrecurringcutenessaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringCutenessActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringsupertriviaaction', aliases = [ 'addrecurringtriviaaction' ])
    async def command_addrecurringsupertriviaaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringSuperTriviaActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringweatheraction')
    async def command_addrecurringweatheraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringWeatherActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringwordofthedayaction', aliases = [ 'addrecurringwordaction', 'addrecurringwotdaction' ])
    async def command_addrecurringwordofthedayaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringWordOfTheDayActionCommand.handleChatCommand(context)

    @commands.command(name = 'addsoundalertcheeraction', aliases = [ 'addsoundcheeraction' ])
    async def command_addsoundalertcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addSoundAlertCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addtimeoutcheeraction')
    async def command_addtimeoutcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTimeoutCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addtriviaanswer')
    async def command_addtriviaanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaAnswerCommand.handleChatCommand(context)

    @commands.command(name = 'addtriviacontroller')
    async def command_addtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'adduser')
    async def command_adduser(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addUserCommand.handleCommand(context)

    @commands.command(name = 'anivtimeouts')
    async def command_anivtimeouts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__anivTimeoutsCommand.handleChatCommand(context)

    @commands.command(name = 'answer', aliases = [ 'ANSWER', 'Answer', 'a', 'A' ])
    async def command_answer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__answerCommand.handleChatCommand(context)

    @commands.command(name = 'bantriviaquestion', aliases = [ 'bantrivia' ])
    async def command_bantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__banTriviaQuestionCommand.handleChatCommand(context)

    @commands.command(name = 'beans')
    async def command_beans(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__beanInstructionsCommand.handleChatCommand(context)

    @commands.command(name = 'beanstats')
    async def command_beanstats(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__beanStatsCommand.handleChatCommand(context)

    @commands.command(name = 'clearcaches')
    async def command_clearcaches(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearCachesCommand.handleChatCommand(context)

    @commands.command(name = 'clearsupertriviaqueue', aliases = [ 'cleartriviaqueue' ])
    async def command_clearsupertriviaqueue(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearSuperTriviaQueueCommand.handleChatCommand(context)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__commandsCommand.handleChatCommand(context)

    @commands.command(name = 'confirm')
    async def command_confirm(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__confirmCommand.handleCommand(context)

    @commands.command(name = 'crowdcontrol')
    async def command_crowdcontrol(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__crowdControlCommand.handleChatCommand(context)

    @commands.command(name = 'cuteness', aliases = [ 'CUTENESS', 'Cuteness' ])
    async def command_cuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessCommand.handleChatCommand(context)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessChampionsCommand.handleChatCommand(context)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessHistoryCommand.handleChatCommand(context)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cynanSourceCommand.handleCommand(context)

    @commands.command(name = 'deletecheeraction', aliases = [ 'removecheeraction' ])
    async def command_deletecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'deletetriviaanswers')
    async def command_deletetriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteTriviaAnswersCommand.handleChatCommand(context)

    @commands.command(name = 'disablecheeraction')
    async def command_disablecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__disableCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__discordCommand.handleCommand(context)

    @commands.command(name = 'enablecheeraction')
    async def command_enablecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__enableCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'getbannedtriviacontrollers')
    async def command_getbannedtriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getBannedTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'getcheeractions', aliases = [ 'cheeractions' ])
    async def command_getcheeractions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getCheerActionsCommand.handleChatCommand(context)

    @commands.command(name = 'getglobaltriviacontrollers')
    async def command_getglobaltriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getGlobalTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'getrecurringactions', aliases = [ 'recurringactions' ])
    async def command_getrecurringactions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__recurringActionsCommand.handleChatCommand(context)

    @commands.command(name = 'gettriviaanswers', aliases = [ 'triviaanswers' ])
    async def command_gettriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaAnswersCommand.handleChatCommand(context)

    @commands.command(name = 'gettriviacontrollers')
    async def command_gettriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'givecuteness', aliases = [ 'addcuteness' ])
    async def command_givecuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__giveCutenessCommand.handleChatCommand(context)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__jishoCommand.handleChatCommand(context)

    @commands.command(name = 'lorem')
    async def command_lorem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__loremIpsumCommand.handleChatCommand(context)

    @commands.command(name = 'mastodon')
    async def command_mastodon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__mastodonCommand.handleCommand(context)

    @commands.command(name = 'mycuteness', aliases = [ 'mycutenesshistory' ])
    async def command_mycuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__myCutenessCommand.handleChatCommand(context)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pbsCommand.handleCommand(context)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMonCommand.handleCommand(context)

    @commands.command(name = 'pkmove', aliases = [ 'pkmov' ])
    async def command_pkmove(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMoveCommand.handleCommand(context)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__raceCommand.handleCommand(context)

    @commands.command(name = 'removebannedtriviacontroller')
    async def command_removebannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeBannedTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'removeglobaltriviacontroller')
    async def command_removeglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeGlobalTriviaControllerChatCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringcutenessaction', aliases = [ 'deleterecurringcutenessaction' ])
    async def command_removerecurringcutenessaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringCutenessActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringsupertriviaaction', aliases = [ 'deleterecurringsupertriviaaction', 'deleterecurringtriviaaction', 'removerecurringtriviaaction' ])
    async def command_removerecurringsupertriviaaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringSuperTriviaActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringweatheraction', aliases = [ 'deleterecurringweatheraction' ])
    async def command_removeweatherrecurringaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringWeatherActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringwordofthedayaction', aliases = [ 'deleterecurringwordaction', 'deleterecurringwordofthedayaction', 'deleterecurringwotdaction', 'removerecurringwordaction', 'removerecurringwotdaction' ])
    async def command_removerecurringwordofthedayaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringWordOfTheDayActionCommand.handleChatCommand(context)

    @commands.command(name = 'removetriviacontroller')
    async def command_removetriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeTriviaControllerChatCommand.handleChatCommand(context)

    @commands.command(name = 'setfuntoontoken')
    async def command_setfuntoontoken(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setFuntoonTokenCommand.handleCommand(context)

    @commands.command(name = 'settwitchcode')
    async def command_settwitchcode(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setTwitchCodeCommand.handleCommand(context)

    @commands.command(name = 'superanswer', aliases = [ 'SUPERANSWER', 'SuperAnswer', 'Superanswer', 'sa', 'SA', 'Sa', 'sA', 'sanswer', 'SANSWER', 'Sanswer' ])
    async def command_superanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superAnswerCommand.handleChatCommand(context)

    @commands.command(name = 'supertrivia', aliases = ['supertrivialotr'])
    async def command_supertrivia(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superTriviaCommand.handleChatCommand(context)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__swQuoteCommand.handleCommand(context)

    @commands.command(name = 'testcheeraction')
    async def command_testcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__testCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__timeCommand.handleChatCommand(context)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__translateCommand.handleChatCommand(context)

    @commands.command(name = 'triviainfo', aliases = [ 'gettriviainfo' ])
    async def command_triviainfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaInfoCommand.handleChatCommand(context)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaScoreCommand.handleChatCommand(context)

    @commands.command(name = 'tts', aliases = [ 'TTS' ])
    async def command_tts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__ttsCommand.handleChatCommand(context)

    @commands.command(name = 'twitchinfo')
    async def command_twitchinfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__twitchInfoCommand.handleCommand(context)

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__twitterCommand.handleCommand(context)

    @commands.command(name = 'unbantriviaquestion')
    async def command_unbantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__unbanTriviaQuestionChatCommand.handleChatCommand(context)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__weatherCommand.handleChatCommand(context)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__wordCommand.handleChatCommand(context)
