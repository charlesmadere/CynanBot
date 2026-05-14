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
from .chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from .chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
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
from .crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from .crowdControl.crowdControlActionHandler import CrowdControlActionHandler
from .crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from .crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from .crowdControl.message.crowdControlMessageListener import CrowdControlMessageListener
from .crowdControl.settings.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from .crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from .language.languagesRepositoryInterface import LanguagesRepositoryInterface
from .location.locationsRepositoryInterface import LocationsRepositoryInterface
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc.administratorProviderInterface import AdministratorProviderInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.generalSettingsRepository import GeneralSettingsRepository
from .misc.startable import Startable
from .mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from .pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .timber.timberInterface import TimberInterface
from .timeout.settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from .trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import \
    OpenTriviaDatabaseSessionTokenRepositoryInterface
from .tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from .twitch.absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .twitch.absTwitchChatHandler import AbsTwitchChatHandler
from .twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from .twitch.absTwitchHypeTrainHandler import AbsTwitchHypeTrainHandler
from .twitch.absTwitchPollHandler import AbsTwitchPollHandler
from .twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from .twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from .twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from .twitch.configuration.absChannelJoinEvent import AbsChannelJoinEvent
from .twitch.configuration.channelJoinListener import ChannelJoinListener
from .twitch.configuration.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from .twitch.configuration.joinChannelsEvent import JoinChannelsEvent
from .twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from .twitch.websocket.listener.twitchWebsocketConnectionsFinishedListener import \
    TwitchWebsocketConnectionsFinishedListener
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from .users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from .users.usersRepositoryInterface import UsersRepositoryInterface


class CynanBot(
    commands.Bot,
    ChannelJoinListener,
    TwitchWebsocketConnectionsFinishedListener,
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
        chatLogger: ChatLoggerInterface,
        chatterInventoryHelper: ChatterInventoryHelperInterface | None,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface | None,
        chatterInventoryMapper: ChatterInventoryMapperInterface | None,
        chatterInventorySettings: ChatterInventorySettingsInterface | None,
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
        languagesRepository: LanguagesRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface | None,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface | None,
        openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface | None,
        pokepediaRepository: PokepediaRepositoryInterface | None,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface | None,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface | None,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChannelJoinHelper: TwitchChannelJoinHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
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
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif chatterInventoryHelper is not None and not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif chatterInventoryIdGenerator is not None and not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif chatterInventoryMapper is not None and not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif chatterInventorySettings is not None and not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
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
        elif pokepediaRepository is not None and not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutActionSettings is not None and not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif timeoutImmuneUserIdsRepository is not None and not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChannelJoinHelper, TwitchChannelJoinHelperInterface):
            raise TypeError(f'twitchChannelJoinHelper argument is malformed: \"{twitchChannelJoinHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
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
        self.__crowdControlActionHandler: Final[CrowdControlActionHandler | None] = crowdControlActionHandler
        self.__crowdControlMachine: Final[CrowdControlMachineInterface | None] = crowdControlMachine
        self.__crowdControlMessageListener: Final[CrowdControlMessageListener | None] = crowdControlMessageListener
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelJoinHelper: Final[TwitchChannelJoinHelperInterface] = twitchChannelJoinHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchWebsocketClient: Final[TwitchWebsocketClientInterface] = twitchWebsocketClient
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
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

        if self.__twitchWebsocketClient is not None:
            self.__twitchWebsocketClient.setConnectionsFinishedListener(self)
            self.__twitchWebsocketClient.start()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event}')
        await self.join_channels(event.channels)

    async def onWebsocketConnectionsFinished(self, userIds: Collection[str]):
        self.__timber.log('CynanBot', f'Finished establishing Twitch websocket connections ({userIds=})')

        await self.waitForReady()

        if self.__crowdControlMachine is not None:
            self.__crowdControlMachine.setActionHandler(self.__crowdControlActionHandler)
            self.__crowdControlMachine.setMessageListener(self.__crowdControlMessageListener)
            self.__crowdControlMachine.start()

        for startable in self.__startables:
            startable.start()

        self.__timber.log('CynanBot', f'Finished starting all {len(self.__startables)} startable(s)')

    async def waitForReady(self):
        await self.wait_for_ready()
