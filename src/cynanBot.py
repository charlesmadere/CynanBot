import traceback
from asyncio import AbstractEventLoop
from typing import Any, Collection, Final

from frozenlist import FrozenList
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

from .aniv.helpers.anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from .aniv.helpers.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from .aniv.presenters.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from .aniv.repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from .aniv.settings.anivSettingsInterface import AnivSettingsInterface
from .asplodieStats.asplodieStatsPresenter import AsplodieStatsPresenter
from .asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from .chatLogger.chatLoggerInterface import ChatLoggerInterface
from .chatterInventory.configuration.absChatterItemEventHandler import AbsChatterItemEventHandler
from .chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from .chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from .chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from .chatterInventory.machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from .chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from .chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from .chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from .chatterPreferredName.repositories.chatterPreferredNameRepositoryInterface import \
    ChatterPreferredNameRepositoryInterface
from .chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from .chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from .chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from .chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from .chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from .chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from .crowdControl.bizhawk.bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from .crowdControl.crowdControlActionHandler import CrowdControlActionHandler
from .crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from .crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from .crowdControl.message.crowdControlMessageListener import CrowdControlMessageListener
from .crowdControl.settings.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from .crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from .language.languagesRepositoryInterface import LanguagesRepositoryInterface
from .language.translationHelperInterface import TranslationHelperInterface
from .location.locationsRepositoryInterface import LocationsRepositoryInterface
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc.administratorProviderInterface import AdministratorProviderInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.generalSettingsRepository import GeneralSettingsRepository
from .misc.startable import Startable
from .mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from .pixelsDice.listeners.pixelsDiceEventListener import PixelsDiceEventListener
from .pixelsDice.machine.pixelsDiceMachineInterface import PixelsDiceMachineInterface
from .pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from .recurringActions.configuration.absRecurringActionsEventHandler import AbsRecurringActionsEventHandler
from .recurringActions.recurringActionsHelperInterface import RecurringActionsHelperInterface
from .recurringActions.recurringActionsMachineInterface import RecurringActionsMachineInterface
from .recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from .recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .timber.timberInterface import TimberInterface
from .timeout.configuration.absTimeoutEventHandler import AbsTimeoutEventHandler
from .timeout.guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from .timeout.settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from .trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from .trivia.banned.bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from .trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from .trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import \
    OpenTriviaDatabaseSessionTokenRepositoryInterface
from .trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from .tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from .tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from .tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from .ttsMonster.tokens.ttsMonsterTokensRepositoryInterface import \
    TtsMonsterTokensRepositoryInterface
from .twitch.absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .twitch.absTwitchChatHandler import AbsTwitchChatHandler
from .twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from .twitch.absTwitchHypeTrainHandler import AbsTwitchHypeTrainHandler
from .twitch.absTwitchPollHandler import AbsTwitchPollHandler
from .twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from .twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from .twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from .twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from .twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from .twitch.configuration.absChannelJoinEvent import AbsChannelJoinEvent
from .twitch.configuration.channelJoinListener import ChannelJoinListener
from .twitch.configuration.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from .twitch.configuration.joinChannelsEvent import JoinChannelsEvent
from .twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from .twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from .twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from .twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from .twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from .twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from .twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from .twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from .twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from .twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from .twitch.twitchWebsocketDataBundleHandler import TwitchWebsocketDataBundleHandler
from .twitch.websocket.settings.twitchWebsocketSettingsRepositoryInterface import \
    TwitchWebsocketSettingsRepositoryInterface
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from .users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from .users.usersRepositoryInterface import UsersRepositoryInterface
from .websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface


class CynanBot(
    commands.Bot,
    ChannelJoinListener,
    TwitchConnectionReadinessProvider,
):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        twitchChannelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None,
        twitchChatHandler: AbsTwitchChatHandler | None,
        twitchFollowHandler: AbsTwitchFollowHandler | None,
        twitchHypeTrainHandler: AbsTwitchHypeTrainHandler | None,
        twitchPollHandler: AbsTwitchPollHandler | None,
        twitchPredictionHandler: AbsTwitchPredictionHandler | None,
        twitchRaidHandler: AbsTwitchRaidHandler | None,
        twitchSubscriptionHandler: AbsTwitchSubscriptionHandler | None,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface | None,
        administratorProvider: AdministratorProviderInterface,
        anivCopyMessageTimeoutScoreHelper: AnivCopyMessageTimeoutScoreHelperInterface | None,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface | None,
        anivSettings: AnivSettingsInterface | None,
        asplodieStatsPresenter: AsplodieStatsPresenter | None,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface | None,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface | None,
        bannedWordsRepository: BannedWordsRepositoryInterface | None,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface | None,
        chatLogger: ChatLoggerInterface,
        chatterInventoryHelper: ChatterInventoryHelperInterface | None,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface | None,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface | None,
        chatterInventoryMapper: ChatterInventoryMapperInterface | None,
        chatterInventorySettings: ChatterInventorySettingsInterface | None,
        chatterItemEventHandler: AbsChatterItemEventHandler | None,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface | None,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface | None,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface | None,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter | None,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface | None,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface | None,
        chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface | None,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        crowdControlActionHandler: CrowdControlActionHandler | None,
        crowdControlAutomator: CrowdControlAutomatorInterface | None,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface | None,
        crowdControlMachine: CrowdControlMachineInterface | None,
        crowdControlMessageListener: CrowdControlMessageListener | None,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface | None,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface | None,
        generalSettingsRepository: GeneralSettingsRepository,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface | None,
        languagesRepository: LanguagesRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface | None,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface | None,
        openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface | None,
        pixelsDiceEventListener: PixelsDiceEventListener | None,
        pixelsDiceMachine: PixelsDiceMachineInterface | None,
        pokepediaRepository: PokepediaRepositoryInterface | None,
        recurringActionsEventHandler: AbsRecurringActionsEventHandler | None,
        recurringActionsHelper: RecurringActionsHelperInterface | None,
        recurringActionsMachine: RecurringActionsMachineInterface | None,
        recurringActionsRepository: RecurringActionsRepositoryInterface | None,
        recurringActionsWizard: RecurringActionsWizardInterface | None,
        sentMessageLogger: SentMessageLoggerInterface,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface | None,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface | None,
        timeoutActionSettings: TimeoutActionSettingsInterface | None,
        timeoutEventHandler: AbsTimeoutEventHandler | None,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface | None,
        timeZoneRepository: TimeZoneRepositoryInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface | None,
        translationHelper: TranslationHelperInterface | None,
        trollmojiHelper: TrollmojiHelperInterface | None,
        trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface | None,
        ttsJsonMapper: TtsJsonMapperInterface | None,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface | None,
        ttsMonsterTokensRepository: TtsMonsterTokensRepositoryInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface | None,
        twitchApiService: TwitchApiServiceInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChannelJoinHelper: TwitchChannelJoinHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface | None,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface | None,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface | None,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface | None,
        twitchWebsocketSettingsRepository: TwitchWebsocketSettingsRepositoryInterface | None,
        useChatterItemHelper: UseChatterItemHelperInterface | None,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        websocketConnectionServer: WebsocketConnectionServerInterface | None,
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
        elif twitchChannelPointRedemptionHandler is not None and not isinstance(twitchChannelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise TypeError(f'twitchChannelPointRedemptionHandler argument is malformed: \"{twitchChannelPointRedemptionHandler}\"')
        elif twitchChatHandler is not None and not isinstance(twitchChatHandler, AbsTwitchChatHandler):
            raise TypeError(f'twitchChatHandler argument is malformed: \"{twitchChatHandler}\"')
        elif twitchFollowHandler is not None and not isinstance(twitchFollowHandler, AbsTwitchFollowHandler):
            raise TypeError(f'twitchFollowHandler argument is malformed: \"{twitchFollowHandler}\"')
        elif twitchHypeTrainHandler is not None and not isinstance(twitchHypeTrainHandler, AbsTwitchHypeTrainHandler):
            raise TypeError(f'twitchHypeTrainHandler argument is malformed: \"{twitchHypeTrainHandler}\"')
        elif twitchPollHandler is not None and not isinstance(twitchPollHandler, AbsTwitchPollHandler):
            raise TypeError(f'twitchPollHandler argument is malformed: \"{twitchPollHandler}\"')
        elif twitchPredictionHandler is not None and not isinstance(twitchPredictionHandler, AbsTwitchPredictionHandler):
            raise TypeError(f'twitchPredictionHandler argument is malformed: \"{twitchPredictionHandler}\"')
        elif twitchRaidHandler is not None and not isinstance(twitchRaidHandler, AbsTwitchRaidHandler):
            raise TypeError(f'twitchRaidHandler argument is malformed: \"{twitchRaidHandler}\"')
        elif twitchSubscriptionHandler is not None and not isinstance(twitchSubscriptionHandler, AbsTwitchSubscriptionHandler):
            raise TypeError(f'twitchSubscriptionHandler argument is malformed: \"{twitchSubscriptionHandler}\"')
        elif not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif additionalTriviaAnswersRepository is not None and not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif anivCopyMessageTimeoutScoreHelper is not None and not isinstance(anivCopyMessageTimeoutScoreHelper, AnivCopyMessageTimeoutScoreHelperInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreHelper argument is malformed: \"{anivCopyMessageTimeoutScoreHelper}\"')
        elif anivCopyMessageTimeoutScorePresenter is not None and not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        elif anivSettings is not None and not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif asplodieStatsPresenter is not None and not isinstance(asplodieStatsPresenter, AsplodieStatsPresenter):
            raise TypeError(f'asplodieStatsPresenter argument is malformed: \"{asplodieStatsPresenter}\"')
        elif asplodieStatsRepository is not None and not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise TypeError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif bannedTriviaGameControllersRepository is not None and not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif bizhawkSettingsRepository is not None and not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif chatterInventoryHelper is not None and not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif chatterInventoryIdGenerator is not None and not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif chatterInventoryItemUseMachine is not None and not isinstance(chatterInventoryItemUseMachine, ChatterInventoryItemUseMachineInterface):
            raise TypeError(f'chatterInventoryItemUseMachine argument is malformed: \"{chatterInventoryItemUseMachine}\"')
        elif chatterInventoryMapper is not None and not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif chatterInventorySettings is not None and not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif chatterItemEventHandler is not None and not isinstance(chatterItemEventHandler, AbsChatterItemEventHandler):
            raise TypeError(f'chatterItemEventHandler argument is malformed: \"{chatterItemEventHandler}\"')
        elif chatterPreferredNameHelper is not None and not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif chatterPreferredNameRepository is not None and not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif chatterPreferredNameSettings is not None and not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif chatterPreferredTtsPresenter is not None and not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif chatterPreferredTtsRepository is not None and not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif chatterPreferredTtsSettingsRepository is not None and not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif chatterPreferredTtsUserMessageHelper is not None and not isinstance(chatterPreferredTtsUserMessageHelper, ChatterPreferredTtsUserMessageHelperInterface):
            raise TypeError(f'chatterPreferredTtsUserMessageHelper argument is malformed: \"{chatterPreferredTtsUserMessageHelper}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif crowdControlActionHandler is not None and not isinstance(crowdControlActionHandler, CrowdControlActionHandler):
            raise TypeError(f'crowdControlActionHandler argument is malformed: \"{crowdControlActionHandler}\"')
        elif crowdControlAutomator is not None and not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif crowdControlIdGenerator is not None and not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif crowdControlMachine is not None and not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif crowdControlMessageListener is not None and not isinstance(crowdControlMessageListener, CrowdControlMessageListener):
            raise TypeError(f'crowdControlMessageListener argument is malformed: \"{crowdControlMessageListener}\"')
        elif crowdControlSettingsRepository is not None and not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif crowdControlUserInputUtils is not None and not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
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
        elif pixelsDiceEventListener is not None and not isinstance(pixelsDiceEventListener, PixelsDiceEventListener):
            raise TypeError(f'pixelsDiceEventListener argument is malformed: \"{pixelsDiceEventListener}\"')
        elif pixelsDiceMachine is not None and not isinstance(pixelsDiceMachine, PixelsDiceMachineInterface):
            raise TypeError(f'pixelsDiceMachine argument is malformed:\"{pixelsDiceMachine}\"')
        elif pokepediaRepository is not None and not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif recurringActionsEventHandler is not None and not isinstance(recurringActionsEventHandler, AbsRecurringActionsEventHandler):
            raise TypeError(f'recurringActionsEventHandler argument is malformed: \"{recurringActionsEventHandler}\"')
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
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutActionMachine is not None and not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif timeoutActionSettings is not None and not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif timeoutEventHandler is not None and not isinstance(timeoutEventHandler, AbsTimeoutEventHandler):
            raise TypeError(f'timeoutEventHandler argument is malformed: \"{timeoutEventHandler}\"')
        elif timeoutImmuneUserIdsRepository is not None and not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif toxicTriviaOccurencesRepository is not None and not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif translationHelper is not None and not isinstance(translationHelper, TranslationHelperInterface):
            raise TypeError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif trollmojiHelper is not None and not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif trollmojiSettingsRepository is not None and not isinstance(trollmojiSettingsRepository, TrollmojiSettingsRepositoryInterface):
            raise TypeError(f'trollmojiSettingsRepository argument is malformed: \"{trollmojiSettingsRepository}\"')
        elif ttsJsonMapper is not None and not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif ttsMonsterSettingsRepository is not None and not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif ttsMonsterTokensRepository is not None and not isinstance(ttsMonsterTokensRepository, TtsMonsterTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterTokensRepository argument is malformed: \"{ttsMonsterTokensRepository}\"')
        elif ttsSettingsRepository is not None and not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChannelJoinHelper, TwitchChannelJoinHelperInterface):
            raise TypeError(f'twitchChannelJoinHelper argument is malformed: \"{twitchChannelJoinHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif twitchFriendsUserIdRepository is not None and not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif twitchSubscriptionsRepository is not None and not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif twitchTimeoutHelper is not None and not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif twitchTimeoutRemodHelper is not None and not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif twitchWebsocketClient is not None and not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif twitchWebsocketSettingsRepository is not None and not isinstance(twitchWebsocketSettingsRepository, TwitchWebsocketSettingsRepositoryInterface):
            raise TypeError(f'twitchWebsocketSettingsRepository argument is malformed: \"{twitchWebsocketSettingsRepository}\"')
        elif useChatterItemHelper is not None and not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif startables is not None and not isinstance(startables, Collection):
            raise TypeError(f'startables argument is malformed: \"{startables}\"')

        self.__twitchChannelPointRedemptionHandler: Final[AbsTwitchChannelPointRedemptionHandler | None] = twitchChannelPointRedemptionHandler
        self.__twitchChatHandler: Final[AbsTwitchChatHandler | None] = twitchChatHandler
        self.__twitchFollowHandler: Final[AbsTwitchFollowHandler | None] = twitchFollowHandler
        self.__twitchHypeTrainHandler: Final[AbsTwitchHypeTrainHandler | None] = twitchHypeTrainHandler
        self.__twitchPollHandler: Final[AbsTwitchPollHandler | None] = twitchPollHandler
        self.__twitchPredictionHandler: Final[AbsTwitchPredictionHandler | None] = twitchPredictionHandler
        self.__twitchRaidHandler: Final[AbsTwitchRaidHandler | None] = twitchRaidHandler
        self.__twitchSubscriptionHandler: Final[AbsTwitchSubscriptionHandler | None] = twitchSubscriptionHandler
        self.__authRepository: Final[AuthRepository] = authRepository
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface | None] = chatterInventoryItemUseMachine
        self.__chatterItemEventHandler: Final[AbsChatterItemEventHandler | None] = chatterItemEventHandler
        self.__crowdControlActionHandler: Final[CrowdControlActionHandler | None] = crowdControlActionHandler
        self.__crowdControlMachine: Final[CrowdControlMachineInterface | None] = crowdControlMachine
        self.__crowdControlMessageListener: Final[CrowdControlMessageListener | None] = crowdControlMessageListener
        self.__pixelsDiceEventListener: Final[PixelsDiceEventListener | None] = pixelsDiceEventListener
        self.__pixelsDiceMachine: Final[PixelsDiceMachineInterface | None] = pixelsDiceMachine
        self.__recurringActionsEventHandler: Final[AbsRecurringActionsEventHandler | None] = recurringActionsEventHandler
        self.__recurringActionsMachine: Final[RecurringActionsMachineInterface | None] = recurringActionsMachine
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface | None] = timeoutActionMachine
        self.__timeoutEventHandler: Final[AbsTimeoutEventHandler | None] = timeoutEventHandler
        self.__twitchChannelJoinHelper: Final[TwitchChannelJoinHelperInterface] = twitchChannelJoinHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None = twitchTimeoutRemodHelper
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchWebsocketClient: Final[TwitchWebsocketClientInterface | None] = twitchWebsocketClient
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__websocketConnectionServer: Final[WebsocketConnectionServerInterface | None] = websocketConnectionServer
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
        await self.waitForReady()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'{twitchHandle} is ready!')

        self.__twitchChannelJoinHelper.setChannelJoinListener(self)
        self.__twitchChannelJoinHelper.joinChannels()

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received IRC RECONNECT event')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        self.__timber.log('CynanBot', f'Received new channel join event ({event=})')

        await self.waitForReady()

        if isinstance(event, FinishedJoiningChannelsEvent):
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif isinstance(event, JoinChannelsEvent):
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBot', f'Finished joining channels ({event.allChannels=})')

        await self.waitForReady()

        self.__timber.start()
        self.__twitchTokensRepository.start()
        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__twitchChatMessenger.start()

        if self.__twitchChannelPointRedemptionHandler is not None:
            self.__twitchChannelPointRedemptionHandler.start()

        if self.__chatterItemEventHandler is not None:
            self.__chatterItemEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__chatterInventoryItemUseMachine is not None:
            self.__chatterInventoryItemUseMachine.setEventListener(self.__chatterItemEventHandler)
            self.__chatterInventoryItemUseMachine.start()

        if self.__crowdControlMachine is not None:
            self.__crowdControlMachine.setActionHandler(self.__crowdControlActionHandler)
            self.__crowdControlMachine.setMessageListener(self.__crowdControlMessageListener)
            self.__crowdControlMachine.start()

        if self.__timeoutEventHandler is not None:
            self.__timeoutEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__timeoutActionMachine is not None:
            self.__timeoutActionMachine.setEventListener(self.__timeoutEventHandler)
            self.__timeoutActionMachine.start()

        if self.__twitchTimeoutRemodHelper is not None:
            self.__twitchTimeoutRemodHelper.start()

        if self.__recurringActionsEventHandler is not None:
            self.__recurringActionsEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__recurringActionsMachine is not None:
            self.__recurringActionsMachine.setEventListener(self.__recurringActionsEventHandler)
            self.__recurringActionsMachine.start()

        if self.__pixelsDiceMachine is not None:
            self.__pixelsDiceMachine.setEventListener(self.__pixelsDiceEventListener)
            self.__pixelsDiceMachine.start()

        if self.__websocketConnectionServer is not None:
            self.__websocketConnectionServer.start()

        if self.__twitchWebsocketClient is not None:
            self.__twitchWebsocketClient.setDataBundleListener(TwitchWebsocketDataBundleHandler(
                channelPointRedemptionHandler = self.__twitchChannelPointRedemptionHandler,
                chatHandler = self.__twitchChatHandler,
                followHandler = self.__twitchFollowHandler,
                hypeTrainHandler = self.__twitchHypeTrainHandler,
                pollHandler = self.__twitchPollHandler,
                predictionHandler = self.__twitchPredictionHandler,
                raidHandler = self.__twitchRaidHandler,
                subscriptionHandler = self.__twitchSubscriptionHandler,
                timber = self.__timber,
                userIdsRepository = self.__userIdsRepository,
                usersRepository = self.__usersRepository,
            ))

            self.__twitchWebsocketClient.start()

        for startable in self.__startables:
            startable.start()

        self.__timber.log('CynanBot', f'Finished starting all {len(self.__startables)} startable(s)')

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event}')
        await self.join_channels(event.channels)

    async def waitForReady(self):
        await self.wait_for_ready()
