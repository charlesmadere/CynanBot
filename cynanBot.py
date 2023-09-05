import traceback
from asyncio import AbstractEventLoop
from typing import Any, Dict, List, Optional

from twitchio import Channel, Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.pubsub import PubSubChannelPointsMessage

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from commands import (AbsCommand, AddBannedTriviaControllerCommand,
                      AddGlobalTriviaControllerCommand, AddTriviaAnswerCommand,
                      AddTriviaControllerCommand, AddUserCommand,
                      AnswerCommand, BanTriviaQuestionCommand,
                      ClearCachesCommand, ClearSuperTriviaQueueCommand,
                      CommandsCommand, ConfirmCommand,
                      CutenessChampionsCommand, CutenessCommand,
                      CutenessHistoryCommand, CynanSourceCommand,
                      DeleteTriviaAnswersCommand, DiscordCommand,
                      GetBannedTriviaControllersCommand,
                      GetGlobalTriviaControllersCommand,
                      GetTriviaAnswersCommand, GetTriviaControllersCommand,
                      GiveCutenessCommand, JishoCommand, LoremIpsumCommand,
                      MyCutenessHistoryCommand, PbsCommand, PkMonCommand,
                      PkMoveCommand, RaceCommand, RecurringActionCommand,
                      RecurringActionsCommand,
                      RemoveBannedTriviaControllerCommand,
                      RemoveGlobalTriviaControllerCommand,
                      RemoveTriviaControllerCommand, SetFuntoonTokenCommand,
                      SetTwitchCodeCommand, StubCommand, SuperAnswerCommand,
                      SuperTriviaCommand, SwQuoteCommand, TimeCommand,
                      TranslateCommand, TriviaInfoCommand, TriviaScoreCommand,
                      TwitchInfoCommand, TwitterCommand,
                      UnbanTriviaQuestionCommand, WeatherCommand, WordCommand)
from cutenessUtils import CutenessUtils
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.funtoon.funtoonTokensRepository import \
    FuntoonTokensRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.lruCache import LruCache
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.recurringActions.recurringActionEventListener import \
    RecurringActionEventListener
from CynanBotCommon.recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from CynanBotCommon.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBotCommon.recurringActions.recurringEvent import RecurringEvent
from CynanBotCommon.recurringActions.recurringEventType import \
    RecurringEventType
from CynanBotCommon.recurringActions.superTriviaRecurringEvent import \
    SuperTriviaRecurringEvent
from CynanBotCommon.recurringActions.weatherRecurringEvent import \
    WeatherRecurringEvent
from CynanBotCommon.recurringActions.wordOfTheDayRecurringEvent import \
    WordOfTheDayRecurringEvent
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBotCommon.trivia.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBotCommon.trivia.bannedTriviaGameControllersRepository import \
    BannedTriviaGameControllersRepository
from CynanBotCommon.trivia.bannedWords.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBotCommon.trivia.clearedSuperTriviaQueueTriviaEvent import \
    ClearedSuperTriviaQueueTriviaEvent
from CynanBotCommon.trivia.correctAnswerTriviaEvent import \
    CorrectAnswerTriviaEvent
from CynanBotCommon.trivia.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from CynanBotCommon.trivia.incorrectAnswerTriviaEvent import \
    IncorrectAnswerTriviaEvent
from CynanBotCommon.trivia.invalidAnswerInputTriviaEvent import \
    InvalidAnswerInputTriviaEvent
from CynanBotCommon.trivia.newSuperTriviaGameEvent import \
    NewSuperTriviaGameEvent
from CynanBotCommon.trivia.newTriviaGameEvent import NewTriviaGameEvent
from CynanBotCommon.trivia.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.outOfTimeSuperTriviaEvent import \
    OutOfTimeSuperTriviaEvent
from CynanBotCommon.trivia.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from CynanBotCommon.trivia.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBotCommon.trivia.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from CynanBotCommon.trivia.triviaBanHelper import TriviaBanHelper
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaEventListener import TriviaEventListener
from CynanBotCommon.trivia.triviaEventType import TriviaEventType
from CynanBotCommon.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBotCommon.trivia.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from CynanBotCommon.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBotCommon.twitch.twitchApiService import TwitchApiService
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from events import (AbsEvent, RaidLogEvent, RaidThankEvent, StubEvent,
                    SubGiftThankingEvent)
from generalSettingsRepository import GeneralSettingsRepository
from messages import (AbsMessage, CatJamMessage, ChatLogMessage,
                      DeerForceMessage, EyesMessage, ImytSlurpMessage,
                      JamCatMessage, RatJamMessage, RoachMessage,
                      SchubertWalkMessage, StubMessage)
from pointRedemptions import (AbsPointRedemption, CutenessRedemption,
                              PkmnBattleRedemption, PkmnCatchRedemption,
                              PkmnEvolveRedemption, PkmnShinyRedemption,
                              PotdPointRedemption, StubPointRedemption,
                              SuperTriviaGameRedemption, TriviaGameRedemption)
from triviaUtils import TriviaUtils
from twitch.absChannelJoinEvent import AbsChannelJoinEvent
from twitch.channelJoinEventType import ChannelJoinEventType
from twitch.channelJoinHelper import ChannelJoinHelper
from twitch.channelJoinListener import ChannelJoinListener
from twitch.eventSubUtils import EventSubUtils
from twitch.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from twitch.joinChannelsEvent import JoinChannelsEvent
from twitch.pubSubUtils import PubSubUtils
from twitch.twitchChannel import TwitchChannel
from twitch.twitchConfiguration import TwitchConfiguration
from twitch.twitchUtils import TwitchUtils
from users.modifyUserActionType import ModifyUserActionType
from users.modifyUserData import ModifyUserData
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.modifyUserEventListener import ModifyUserEventListener
from users.user import User
from users.usersRepository import UsersRepository


class CynanBot(commands.Bot, ChannelJoinListener, ModifyUserEventListener, RecurringActionEventListener, TriviaEventListener):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        additionalTriviaAnswersRepository: Optional[AdditionalTriviaAnswersRepositoryInterface],
        administratorProvider: AdministratorProviderInterface,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelper,
        bannedTriviaGameControllersRepository: Optional[BannedTriviaGameControllersRepository],
        bannedWordsRepository: Optional[BannedWordsRepositoryInterface],
        channelJoinHelper: ChannelJoinHelper,
        chatLogger: Optional[ChatLogger],
        cutenessRepository: Optional[CutenessRepository],
        cutenessUtils: Optional[CutenessUtils],
        funtoonRepository: Optional[FuntoonRepository],
        funtoonTokensRepository: Optional[FuntoonTokensRepository],
        generalSettingsRepository: GeneralSettingsRepository,
        isLiveOnTwitchRepository: Optional[IsLiveOnTwitchRepositoryInterface],
        jishoHelper: Optional[JishoHelper],
        languagesRepository: LanguagesRepository,
        locationsRepository: Optional[LocationsRepository],
        modifyUserDataHelper: ModifyUserDataHelper,
        openTriviaDatabaseTriviaQuestionRepository: Optional[OpenTriviaDatabaseTriviaQuestionRepository],
        pokepediaRepository: Optional[PokepediaRepository],
        recurringActionsMachine: RecurringActionsMachineInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        shinyTriviaOccurencesRepository: Optional[ShinyTriviaOccurencesRepository],
        starWarsQuotesRepository: Optional[StarWarsQuotesRepository],
        timber: TimberInterface,
        toxicTriviaOccurencesRepository: Optional[ToxicTriviaOccurencesRepository],
        translationHelper: Optional[TranslationHelper],
        triviaBanHelper: Optional[TriviaBanHelper],
        triviaEmoteGenerator: Optional[TriviaEmoteGenerator],
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameControllersRepository: Optional[TriviaGameControllersRepository],
        triviaGameGlobalControllersRepository: Optional[TriviaGameGlobalControllersRepository],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        triviaHistoryRepository: Optional[TriviaHistoryRepository],
        triviaRepository: Optional[TriviaRepository],
        triviaScoreRepository: Optional[TriviaScoreRepository],
        triviaSettingsRepository: Optional[TriviaSettingsRepository],
        triviaUtils: TriviaUtils,
        twitchApiService: TwitchApiService,
        twitchConfiguration: TwitchConfiguration,
        twitchTokensRepository: TwitchTokensRepository,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepository,
        weatherRepository: Optional[WeatherRepository],
        wordOfTheDayRepository: Optional[WordOfTheDayRepository]
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireNick(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(channelJoinHelper, ChannelJoinHelper):
            raise ValueError(f'channelJoinHelper argument is malformed: \"{channelJoinHelper}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(recurringActionsMachine, RecurringActionsMachineInterface):
            raise ValueError(f'recurringActionsMachine argument is malformed: \"{recurringActionsMachine}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise ValueError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchApiService, TwitchApiService):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchConfiguration, TwitchConfiguration):
            raise ValueError(f'twitchConfiguration argument is malformed: \"{twitchConfiguration}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepository):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__authRepository: AuthRepository = authRepository
        self.__channelJoinHelper: ChannelJoinHelper = channelJoinHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__recurringActionsMachine: RecurringActionsMachineInterface = recurringActionsMachine
        self.__timber: TimberInterface = timber
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaRepository: Optional[TriviaRepository] = triviaRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchConfiguration: TwitchConfiguration = twitchConfiguration
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__channelPointsLruCache: LruCache = LruCache(64)

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__addUserCommand: AbsCommand = AddUserCommand(administratorProvider, modifyUserDataHelper, timber, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository)
        self.__clearCachesCommand: AbsCommand = ClearCachesCommand(administratorProvider, authRepository, bannedWordsRepository, funtoonTokensRepository, generalSettingsRepository, isLiveOnTwitchRepository, locationsRepository, modifyUserDataHelper, openTriviaDatabaseTriviaQuestionRepository, timber, triviaSettingsRepository, twitchTokensRepository, twitchUtils, usersRepository, weatherRepository, wordOfTheDayRepository)
        self.__commandsCommand: AbsCommand = CommandsCommand(generalSettingsRepository, timber, triviaUtils, twitchUtils, usersRepository)
        self.__confirmCommand: AbsCommand = ConfirmCommand(administratorProvider, modifyUserDataHelper, timber, twitchUtils, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(timber, twitchUtils, usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(timber, twitchUtils, usersRepository)
        self.__loremIpsumCommand: AbsCommand = LoremIpsumCommand(timber, twitchUtils, usersRepository)
        self.__pbsCommand: AbsCommand = PbsCommand(timber, twitchUtils, usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(timber, twitchUtils, usersRepository)
        self.__recurringActionCommand: AbsCommand = RecurringActionCommand(administratorProvider, languagesRepository, recurringActionsRepository, timber, twitchUtils, usersRepository)
        self.__recurringActionsCommand: AbsCommand = RecurringActionsCommand(administratorProvider, recurringActionsRepository, timber, twitchUtils, usersRepository)
        self.__setTwitchCodeCommand: AbsCommand = SetTwitchCodeCommand(administratorProvider, timber, twitchTokensRepository, twitchUtils, usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(timber, twitchUtils, usersRepository)
        self.__twitchInfoCommand: AbsCommand = TwitchInfoCommand(administratorProvider, timber, twitchApiService, authRepository, twitchTokensRepository, twitchUtils, usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(timber, twitchUtils, usersRepository)

        if bannedTriviaGameControllersRepository is None or triviaUtils is None:
            self.__addBannedTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getBannedTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeBannedTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addBannedTriviaControllerCommand: AbsCommand = AddBannedTriviaControllerCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)
            self.__getBannedTriviaControllersCommand: AbsCommand = GetBannedTriviaControllersCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, triviaUtils, twitchUtils, usersRepository)
            self.__removeBannedTriviaControllerCommand: AbsCommand = RemoveBannedTriviaControllerCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)

        if triviaGameGlobalControllersRepository is None or triviaUtils is None:
            self.__addGlobalTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getGlobalTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeGlobalTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addGlobalTriviaControllerCommand: AbsCommand = AddGlobalTriviaControllerCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)
            self.__getGlobalTriviaControllersCommand: AbsCommand = GetGlobalTriviaControllersCommand(administratorProvider,  timber, triviaGameGlobalControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeGlobalTriviaControllerCommand: AbsCommand = RemoveGlobalTriviaControllerCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or triviaGameBuilder is None or triviaGameMachine is None or triviaSettingsRepository is None or triviaScoreRepository is None or triviaUtils is None:
            self.__addTriviaAnswerCommand: AbsCommand = StubCommand()
            self.__answerCommand: AbsCommand = StubCommand()
            self.__deleteTriviaAnswersCommand: AbsCommand = StubCommand()
            self.__getTriviaAnswersCommand: AbsCommand = StubCommand()
            self.__superAnswerCommand: AbsCommand = StubCommand()
            self.__superTriviaCommand: AbsCommand = StubCommand()
        else:
            self.__addTriviaAnswerCommand: AbsCommand = AddTriviaAnswerCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__answerCommand: AbsCommand = AnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__deleteTriviaAnswersCommand: AbsCommand = DeleteTriviaAnswersCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__getTriviaAnswersCommand: AbsCommand = GetTriviaAnswersCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__superAnswerCommand: AbsCommand = SuperAnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__superTriviaCommand: AbsCommand = SuperTriviaCommand(generalSettingsRepository, timber, triviaGameBuilder, triviaGameMachine, triviaSettingsRepository, triviaUtils, twitchUtils, usersRepository)

        if cutenessRepository is None or cutenessUtils is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__cutenessChampionsCommand: AbsCommand = StubCommand()
            self.__cutenessHistoryCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessHistoryCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsCommand = CutenessChampionsCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, usersRepository)
            self.__cutenessHistoryCommand: AbsCommand = CutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, timber, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__myCutenessHistoryCommand: AbsCommand = MyCutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)

        if funtoonTokensRepository is None:
            self.__setFuntoonTokenCommand: AbsCommand = StubCommand()
        else:
            self.__setFuntoonTokenCommand: AbsCommand = SetFuntoonTokenCommand(administratorProvider, funtoonTokensRepository, timber, twitchUtils, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsCommand = StubCommand()
        else:
            self.__jishoCommand: AbsCommand = JishoCommand(generalSettingsRepository, jishoHelper, timber, twitchUtils, usersRepository)

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
            self.__translateCommand: AbsCommand = StubCommand()
        else:
            self.__translateCommand: AbsCommand = TranslateCommand(generalSettingsRepository, languagesRepository, timber, translationHelper, twitchUtils, usersRepository)

        if triviaGameControllersRepository is None or triviaUtils is None:
            self.__addTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addTriviaControllerCommand: AbsCommand = AddTriviaControllerCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)
            self.__getTriviaControllersCommand: AbsCommand = GetTriviaControllersCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeTriviaControllerCommand: AbsCommand = RemoveTriviaControllerCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)

        if triviaGameMachine is None or triviaUtils is None:
            self.__clearSuperTriviaQueueCommand: AbsCommand = StubCommand()
        else:
            self.__clearSuperTriviaQueueCommand: AbsCommand = ClearSuperTriviaQueueCommand(generalSettingsRepository, timber, triviaGameMachine, triviaUtils, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or shinyTriviaOccurencesRepository is None or toxicTriviaOccurencesRepository is None or triviaBanHelper is None or triviaEmoteGenerator is None or triviaHistoryRepository is None or triviaScoreRepository is None or triviaUtils is None:
            self.__banTriviaQuestionCommand: AbsCommand = StubCommand()
            self.__triviaInfoCommand: AbsCommand = StubCommand()
            self.__triviaScoreCommand: AbsCommand = StubCommand()
            self.__unbanTriviaQuestionCommand: AbsCommand = StubCommand()
        else:
            self.__banTriviaQuestionCommand: AbsCommand = BanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaInfoCommand: AbsCommand = TriviaInfoCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaScoreCommand: AbsCommand = TriviaScoreCommand(generalSettingsRepository, shinyTriviaOccurencesRepository, timber, toxicTriviaOccurencesRepository, triviaScoreRepository, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__unbanTriviaQuestionCommand: AbsCommand = UnbanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)

        if locationsRepository is None or weatherRepository is None:
            self.__weatherCommand: AbsCommand = StubCommand()
        else:
            self.__weatherCommand: AbsCommand = WeatherCommand(generalSettingsRepository, locationsRepository, timber, twitchUtils, usersRepository, weatherRepository)

        if wordOfTheDayRepository is None:
            self.__wordCommand: AbsCommand = StubCommand()
        else:
            self.__wordCommand: AbsCommand = WordCommand(generalSettingsRepository, languagesRepository, timber, twitchUtils, usersRepository, wordOfTheDayRepository)

        #############################################
        ## Initialization of event handler objects ##
        #############################################

        if chatLogger is None:
            self.__raidLogEvent: AbsEvent = StubEvent()
        else:
            self.__raidLogEvent: AbsEvent = RaidLogEvent(chatLogger, timber)

        self.__raidThankEvent: AbsEvent = RaidThankEvent(generalSettingsRepository, timber, twitchUtils)
        self.__subGiftThankingEvent: AbsEvent = SubGiftThankingEvent(generalSettingsRepository, timber, authRepository, twitchUtils)

        ###############################################
        ## Initialization of message handler objects ##
        ###############################################

        self.__catJamMessage: AbsMessage = CatJamMessage(generalSettingsRepository, timber, twitchUtils)
        self.__deerForceMessage: AbsMessage = DeerForceMessage(generalSettingsRepository, timber, twitchUtils)
        self.__eyesMessage: AbsMessage = EyesMessage(generalSettingsRepository, timber, twitchUtils)
        self.__imytSlurpMessage: AbsMessage = ImytSlurpMessage(generalSettingsRepository, timber, twitchUtils)
        self.__jamCatMessage: AbsMessage = JamCatMessage(generalSettingsRepository, timber, twitchUtils)
        self.__ratJamMessage: AbsMessage = RatJamMessage(generalSettingsRepository, timber, twitchUtils)
        self.__roachMessage: AbsMessage = RoachMessage(generalSettingsRepository, timber, twitchUtils)
        self.__schubertWalkMessage: AbsMessage = SchubertWalkMessage(generalSettingsRepository, timber, twitchUtils)

        if chatLogger is None:
            self.__chatLogMessage: AbsMessage = StubMessage()
        else:
            self.__chatLogMessage: AbsMessage = ChatLogMessage(chatLogger)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        self.__potdPointRedemption: AbsPointRedemption = PotdPointRedemption(timber, twitchUtils)

        if cutenessRepository is None:
            self.__cutenessPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsPointRedemption = CutenessRedemption(cutenessRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = StubPointRedemption()
            self.__pkmnCatchPointRedemption: AbsPointRedemption = StubPointRedemption()
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = StubPointRedemption()
            self.__pkmnShinyPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = PkmnBattleRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnCatchPointRedemption: AbsPointRedemption = PkmnCatchRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = PkmnEvolveRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnShinyPointRedemption: AbsPointRedemption = PkmnShinyRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if cutenessRepository is None or triviaGameBuilder is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__superTriviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
            self.__triviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__superTriviaGamePointRedemption: AbsPointRedemption = SuperTriviaGameRedemption(timber, triviaGameBuilder, triviaGameMachine)
            self.__triviaGamePointRedemption: AbsPointRedemption = TriviaGameRedemption(timber, triviaGameBuilder, triviaGameMachine)

        generalSettings = self.__generalSettingsRepository.getAll()

        ########################################
        ## Initialization of EventSub objects ##
        ########################################

        self.__eventSubUtils: Optional[EventSubUtils] = None
        if generalSettings.isEventSubEnabled():
            # TODO
            pass

        ######################################
        ## Initialization of PubSub objects ##
        ######################################

        self.__pubSubUtils: Optional[PubSubUtils] = None
        if generalSettings.isPubSubEnabled():
            self.__pubSubUtils = PubSubUtils(
                backgroundTaskHelper = backgroundTaskHelper,
                client = self,
                generalSettingsRepository = generalSettingsRepository,
                timber = timber,
                twitchTokensRepositoryInterface = twitchTokensRepository,
                userIdsRepository = userIdsRepository,
                usersRepositoryInterface = usersRepository
            )

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireNick()}')

    async def event_channel_join_failure(self, channel: str):
        userId = await self.__userIdsRepository.fetchUserId(channel)
        user: Optional[User] = None

        try:
            user = await self.__usersRepository.getUserAsync(channel)
        except:
            pass

        self.__timber.log('CynanBot', f'Failed to join channel \"{channel}\" (userId=\"{userId}\") (user=\"{user}\"), disabling this user...')

        await self.__usersRepository.setUserEnabled(
            handle = user.getHandle(),
            enabled = False
        )

        self.__timber.log('CynanBot', f'Finished disabling user \"{user}\" due to channel join failure')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        twitchMessage = self.__twitchConfiguration.getMessage(message)

        if utils.isValidStr(twitchMessage.getContent()):
            generalSettings = await self.__generalSettingsRepository.getAllAsync()

            if generalSettings.isPersistAllUsersEnabled():
                await self.__userIdsRepository.setUser(
                    userId = twitchMessage.getAuthorId(),
                    userName = twitchMessage.getAuthorName()
                )

            twitchUser = await self.__usersRepository.getUserAsync(twitchMessage.getTwitchChannelName())

            await self.__chatLogMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            )

            if await self.__deerForceMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__catJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__eyesMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__imytSlurpMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__jamCatMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__ratJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__roachMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

            if await self.__schubertWalkMessage.handleMessage(
                twitchUser = twitchUser,
                message = twitchMessage
            ):
                return

        await self.handle_commands(message)

    async def event_pubsub_channel_points(self, event: PubSubChannelPointsMessage):
        twitchUserIdStr = str(event.channel_id)
        lruCacheId = f'{twitchUserIdStr}:{event.id}'.lower()

        if self.__channelPointsLruCache.contains(lruCacheId):
            return

        self.__channelPointsLruCache.put(lruCacheId)
        channelPointsMessage = await self.__twitchConfiguration.getChannelPointsMessage(event)
        twitchUser = channelPointsMessage.getTwitchUser()

        self.__timber.log('CynanBot', f'Reward \"{channelPointsMessage.getRewardId()}\" redeemed by {channelPointsMessage.getUserName()}:{channelPointsMessage.getUserId()} in {twitchUser.getHandle()}')

        twitchChannel = await self.__getChannel(twitchUser.getHandle())

        if twitchUser.isCutenessEnabled() and twitchUser.hasCutenessBoosterPacks():
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if twitchUser.isPicOfTheDayEnabled() and channelPointsMessage.getRewardId() == twitchUser.getPicOfTheDayRewardId():
            if await self.__potdPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if twitchUser.isPkmnEnabled():
            if channelPointsMessage.getRewardId() == twitchUser.getPkmnBattleRewardId():
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if twitchUser.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == twitchUser.getPkmnEvolveRewardId():
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == twitchUser.getPkmnShinyRewardId():
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

        if twitchUser.isTriviaGameEnabled() and channelPointsMessage.getRewardId() == twitchUser.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if twitchUser.isSuperTriviaGameEnabled() and channelPointsMessage.getRewardId() == twitchUser.getSuperTriviaGameRewardId():
            if await self.__superTriviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

    async def event_pubsub_error(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub error: {tags}')

    async def event_pubsub_nonce(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub nonce: {tags}')

    async def event_pubsub_pong(self):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isPubSubPongLoggingEnabled():
            self.__timber.log('CynanBot', f'Received PubSub pong')

    async def event_raw_data(self, data: str):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isRawEventDataLoggingEnabled():
            self.__timber.log('CynanBot', f'event_raw_data(): (data=\"{data}\")')

    async def event_raw_usernotice(self, channel: Channel, tags: Dict[str, Any]):
        twitchChannel = self.__twitchConfiguration.getChannel(channel)
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isDebugLoggingEnabled():
            self.__timber.log('CynanBot', f'event_raw_usernotice(): (channel=\"{twitchChannel}\") (tags=\"{tags}\")')

        msgId = utils.getStrFromDict(tags, 'msg-id', fallback = '')

        if not utils.isValidStr(msgId):
            return

        twitchUser = await self.__usersRepository.getUserAsync(channel.name)

        if msgId == 'raid':
            await self.__raidLogEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )

            await self.__raidThankEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )
        elif msgId == 'subgift' or msgId == 'anonsubgift':
            await self.__subGiftThankingEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )

    async def event_ready(self):
        await self.wait_for_ready()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'{twitchHandle} is ready!')

        self.__channelJoinHelper.setChannelJoinListener(self)
        self.__channelJoinHelper.joinChannels()
        self.__modifyUserDataHelper.setModifyUserEventListener(self)

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received new reconnect event')

        await self.wait_for_ready()

        if self.__pubSubUtils is not None:
            await self.__pubSubUtils.forceFullRefresh()

    async def event_usernotice_subscription(self, metadata):
        self.__timber.log('CynanBot', f'event_usernotice_subscription(): (metadata=\"{metadata}\")')

    async def __getChannel(self, twitchChannel: str) -> TwitchChannel:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

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

    async def onModifyUserEvent(self, event: ModifyUserData):
        self.__timber.log('CynanBot', f'Received new modify user data event: {event.toStr()}')

        await self.wait_for_ready()

        if event.getActionType() is ModifyUserActionType.ADD:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.join_channels(channels)
        elif event.getActionType() is ModifyUserActionType.REMOVE:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.part_channels(channels)
        else:
            raise RuntimeError(f'unknown ModifyUserActionType: \"{event.getActionType()}\"')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        eventType = event.getEventType()
        self.__timber.log('CynanBot', f'Received new channel join event: \"{eventType}\"')

        await self.wait_for_ready()

        if eventType is ChannelJoinEventType.FINISHED:
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif eventType is ChannelJoinEventType.JOIN:
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBot', f'Finished joining channels: {event.getAllChannels()}')

        if self.__triviaRepository is not None:
            self.__triviaRepository.startSpooler()

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self)
            self.__triviaGameMachine.startMachine()

        if self.__eventSubUtils is not None:
            self.__eventSubUtils.startEventSub()

        if self.__pubSubUtils is not None:
            self.__pubSubUtils.startPubSub()

        if self.__recurringActionsMachine is not None:
            self.__recurringActionsMachine.setEventListener(self)
            self.__recurringActionsMachine.startMachine()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event.getChannels()}')
        await self.join_channels(event.getChannels())

    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        eventType = event.getEventType()
        self.__timber.log('CynanBot', f'Received new recurring action event: \"{eventType}\"')

        await self.wait_for_ready()

        if eventType is RecurringEventType.SUPER_TRIVIA:
            await self.__handleSuperTriviaRecurringActionEvent(event)
        elif eventType is RecurringEventType.WEATHER:
            await self.__handleWeatherRecurringActionEvent(event)
        elif eventType is RecurringEventType.WORD_OF_THE_DAY:
            await self.__handleWordOfTheDayRecurringActionEvent(event)

    async def __handleSuperTriviaRecurringActionEvent(self, event: SuperTriviaRecurringEvent):
        if not isinstance(event, SuperTriviaRecurringEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, 'Super trivia starting soon!')

    async def __handleWeatherRecurringActionEvent(self, event: WeatherRecurringEvent):
        if not isinstance(event, WeatherRecurringEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, event.getWeatherReport().toStr())

    async def __handleWordOfTheDayRecurringActionEvent(self, event: WordOfTheDayRecurringEvent):
        if not isinstance(event, WordOfTheDayRecurringEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, event.getWordOfTheDayResponse().toStr())

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        eventType = event.getTriviaEventType()
        self.__timber.log('CynanBot', f'Received new trivia event: \"{eventType}\"')

        await self.wait_for_ready()

        if eventType is TriviaEventType.CLEARED_SUPER_TRIVIA_QUEUE:
            await self.__handleClearedSuperTriviaQueueTriviaEvent(event)
        elif eventType is TriviaEventType.CORRECT_ANSWER:
            await self.__handleCorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionTriviaEvent(event)
        elif eventType is TriviaEventType.GAME_OUT_OF_TIME:
            await self.__handleGameOutOfTimeTriviaEvent(event)
        elif eventType is TriviaEventType.INCORRECT_ANSWER:
            await self.__handleIncorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.INVALID_ANSWER_INPUT:
            await self.__handleInvalidAnswerInputTriviaEvent(event)
        elif eventType is TriviaEventType.NEW_GAME:
            await self.__handleNewTriviaGameEvent(event)
        elif eventType is TriviaEventType.NEW_SUPER_GAME:
            await self.__handleNewSuperTriviaGameEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_CORRECT_ANSWER:
            await self.__handleSuperGameCorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_OUT_OF_TIME:
            await self.__handleSuperGameOutOfTimeTriviaEvent(event)

    async def __handleClearedSuperTriviaQueueTriviaEvent(self, event: ClearedSuperTriviaQueueTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getClearedSuperTriviaQueueMessage(
            numberOfGamesRemoved = event.getNumberOfGamesRemoved()
        ))

    async def __handleCorrectAnswerTriviaEvent(self, event: CorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = event.getCutenessResult(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleFailedToFetchQuestionTriviaEvent(self, event: FailedToFetchQuestionTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(self, event: FailedToFetchQuestionSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameOutOfTimeTriviaEvent(self, event: OutOfTimeTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleIncorrectAnswerTriviaEvent(self, event: IncorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleInvalidAnswerInputTriviaEvent(self, event: InvalidAnswerInputTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleNewTriviaGameEvent(self, event: NewTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleNewSuperTriviaGameEvent(self, event: NewSuperTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleSuperGameCorrectAnswerTriviaEvent(self, event: CorrectSuperAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = event.getCutenessResult(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            userName = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.getToxicTriviaPunishmentResult(),
            emote = event.getEmote()
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleSuperGameOutOfTimeTriviaEvent(self, event: OutOfTimeSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.getToxicTriviaPunishmentResult(),
            emote = event.getEmote()
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    @commands.command(name = 'addbannedtriviacontroller')
    async def command_addbannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addBannedTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'addglobaltriviacontroller')
    async def command_addglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGlobalTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'addtriviaanswer')
    async def command_addtriviaanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaAnswerCommand.handleCommand(context)

    @commands.command(name = 'addtriviacontroller')
    async def command_addtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'adduser')
    async def command_adduser(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addUserCommand.handleCommand(context)

    @commands.command(name = 'answer', aliases = [ 'ANSWER', 'a', 'A' ])
    async def command_answer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__answerCommand.handleCommand(context)

    @commands.command(name = 'bantriviaquestion')
    async def command_bantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__banTriviaQuestionCommand.handleCommand(context)

    @commands.command(name = 'clearcaches')
    async def command_clearcaches(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearCachesCommand.handleCommand(context)

    @commands.command(name = 'clearsupertriviaqueue')
    async def command_clearsupertriviaqueue(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearSuperTriviaQueueCommand.handleCommand(context)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__commandsCommand.handleCommand(context)

    @commands.command(name = 'confirm')
    async def command_confirm(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__confirmCommand.handleCommand(context)

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessCommand.handleCommand(context)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessChampionsCommand.handleCommand(context)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessHistoryCommand.handleCommand(context)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cynanSourceCommand.handleCommand(context)

    @commands.command(name = 'deletetriviaanswers')
    async def command_deletetriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteTriviaAnswersCommand.handleCommand(context)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__discordCommand.handleCommand(context)

    @commands.command(name = 'getbannedtriviacontrollers')
    async def command_getbannedtriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getBannedTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'getglobaltriviacontrollers')
    async def command_getglobaltriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getGlobalTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'gettriviaanswers')
    async def command_gettriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaAnswersCommand.handleCommand(context)

    @commands.command(name = 'gettriviacontrollers')
    async def command_gettriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__giveCutenessCommand.handleCommand(context)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__jishoCommand.handleCommand(context)

    @commands.command(name = 'lorem')
    async def command_lorem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__loremIpsumCommand.handleCommand(context)

    @commands.command(name = 'mycutenesshistory')
    async def command_mycutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__myCutenessHistoryCommand.handleCommand(context)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pbsCommand.handleCommand(context)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMonCommand.handleCommand(context)

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMoveCommand.handleCommand(context)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__raceCommand.handleCommand(context)

    @commands.command(name = 'recurringaction')
    async def command_recurringaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__recurringActionCommand.handleCommand(context)

    @commands.command(name = 'recurringactions')
    async def command_recurringactions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__recurringActionsCommand.handleCommand(context)

    @commands.command(name = 'removebannedtriviacontroller')
    async def command_removebannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeBannedTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'removeglobaltriviacontroller')
    async def command_removeglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeGlobalTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'removetriviacontroller')
    async def command_removetriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'setfuntoontoken')
    async def command_setfuntoontoken(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setFuntoonTokenCommand.handleCommand(context)

    @commands.command(name = 'settwitchcode')
    async def command_settwitchcode(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setTwitchCodeCommand.handleCommand(context)

    @commands.command(name = 'superanswer', aliases = [ 'SUPERANSWER', 'sa', 'SA', 'sanswer', 'SANSWER' ])
    async def command_superanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superAnswerCommand.handleCommand(context)

    @commands.command(name = 'supertrivia')
    async def command_supertrivia(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superTriviaCommand.handleCommand(context)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__swQuoteCommand.handleCommand(context)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__timeCommand.handleCommand(context)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__translateCommand.handleCommand(context)

    @commands.command(name = 'triviainfo')
    async def command_triviainfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaInfoCommand.handleCommand(context)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaScoreCommand.handleCommand(context)

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
        await self.__unbanTriviaQuestionCommand.handleCommand(context)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__weatherCommand.handleCommand(context)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__wordCommand.handleCommand(context)
