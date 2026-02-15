import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from .contentScanner.bannedWordsRepository import BannedWordsRepository
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .contentScanner.contentScanner import ContentScanner
from .contentScanner.contentScannerInterface import ContentScannerInterface
from .cuteness.cutenessRepository import CutenessRepository
from .cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from .funtoon.apiService.funtoonApiService import FuntoonApiService
from .funtoon.apiService.funtoonApiServiceInterface import FuntoonApiServiceInterface
from .funtoon.funtoonHelper import FuntoonHelper
from .funtoon.funtoonHelperInterface import FuntoonHelperInterface
from .funtoon.jsonMapper.funtoonJsonMapper import FuntoonJsonMapper
from .funtoon.jsonMapper.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from .funtoon.tokens.funtoonTokensRepository import FuntoonTokensRepository
from .funtoon.tokens.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelper import BackgroundTaskHelper
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .network.networkClientProvider import NetworkClientProvider
from .network.requests.requestsClientProvider import RequestsClientProvider
from .pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from .pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from .pkmn.pokepediaRepository import PokepediaRepository
from .pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from .storage.backingDatabase import BackingDatabase
from .storage.jsonFileReader import JsonFileReader
from .storage.linesFileReader import LinesFileReader
from .storage.sqlite.sqliteBackingDatabase import SqliteBackingDatabase
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .trivia.additionalAnswers.additionalTriviaAnswersRepository import AdditionalTriviaAnswersRepository
from .trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from .trivia.answerChecker.triviaAnswerChecker import TriviaAnswerChecker
from .trivia.answerChecker.triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from .trivia.banned.bannedTriviaIdsRepository import BannedTriviaIdsRepository
from .trivia.banned.bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from .trivia.banned.triviaBanHelper import TriviaBanHelper
from .trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from .trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from .trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from .trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from .trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from .trivia.content.triviaContentScanner import TriviaContentScanner
from .trivia.content.triviaContentScannerInterface import TriviaContentScannerInterface
from .trivia.emotes.triviaEmoteGenerator import TriviaEmoteGenerator
from .trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from .trivia.emotes.triviaEmoteRepository import TriviaEmoteRepository
from .trivia.emotes.triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
from .trivia.emotes.twitch.triviaTwitchEmoteHelper import TriviaTwitchEmoteHelper
from .trivia.emotes.twitch.triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from .trivia.events.absTriviaEvent import AbsTriviaEvent
from .trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from .trivia.games.triviaGameStore import TriviaGameStore
from .trivia.history.triviaHistoryRepository import TriviaHistoryRepository
from .trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from .trivia.history.triviaQuestionOccurrencesRepository import TriviaQuestionOccurrencesRepository
from .trivia.misc.triviaDifficultyParser import TriviaDifficultyParser
from .trivia.misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from .trivia.misc.triviaQuestionTypeParser import TriviaQuestionTypeParser
from .trivia.misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from .trivia.misc.triviaSourceParser import TriviaSourceParser
from .trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from .trivia.questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from .trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from .trivia.questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from .trivia.questions.triviaSource import TriviaSource
from .trivia.score.triviaScoreRepository import TriviaScoreRepository
from .trivia.scraper.triviaScraper import TriviaScraper
from .trivia.scraper.triviaScraperInterface import TriviaScraperInterface
from .trivia.settings.triviaSettings import TriviaSettings
from .trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from .trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from .trivia.specialStatus.shinyTriviaOccurencesRepository import ShinyTriviaOccurencesRepository
from .trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from .trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from .trivia.specialStatus.toxicTriviaOccurencesRepository import ToxicTriviaOccurencesRepository
from .trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from .trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from .trivia.triviaDifficulty import TriviaDifficulty
from .trivia.triviaEventListener import TriviaEventListener
from .trivia.triviaFetchOptions import TriviaFetchOptions
from .trivia.triviaGameMachine import TriviaGameMachine
from .trivia.triviaIdGenerator import TriviaIdGenerator
from .trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .trivia.triviaRepositories.bongo.bongoApiService import BongoApiService
from .trivia.triviaRepositories.bongo.bongoJsonParser import BongoJsonParser
from .trivia.triviaRepositories.bongoTriviaQuestionRepository import BongoTriviaQuestionRepository
from .trivia.triviaRepositories.funtoonTriviaQuestionRepository import FuntoonTriviaQuestionRepository
from .trivia.triviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from .trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from .trivia.triviaRepositories.jServiceTriviaQuestionRepository import JServiceTriviaQuestionRepository
from .trivia.triviaRepositories.millionaire.millionaireTriviaQuestionStorage import MillionaireTriviaQuestionStorage
from .trivia.triviaRepositories.millionaire.millionaireTriviaQuestionStorageInterface import \
    MillionaireTriviaQuestionStorageInterface
from .trivia.triviaRepositories.millionaireTriviaQuestionRepository import MillionaireTriviaQuestionRepository
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseApiService import OpenTriviaDatabaseApiService
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseApiServiceInterface import \
    OpenTriviaDatabaseApiServiceInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParser import OpenTriviaDatabaseJsonParser
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParserInterface import \
    OpenTriviaDatabaseJsonParserInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseQuestionFetcher import \
    OpenTriviaDatabaseQuestionFetcher
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseQuestionFetcherInterface import \
    OpenTriviaDatabaseQuestionFetcherInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepository import \
    OpenTriviaDatabaseSessionTokenRepository
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import \
    OpenTriviaDatabaseSessionTokenRepositoryInterface
from .trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionStorage import OpenTriviaQaQuestionStorage
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionStorageInterface import \
    OpenTriviaQaQuestionStorageInterface
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParser import OpenTriviaQaQuestionTypeParser
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParserInterface import \
    OpenTriviaQaQuestionTypeParserInterface
from .trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import OpenTriviaQaTriviaQuestionRepository
from .trivia.triviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from .trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGenerator import PokepediaTriviaQuestionGenerator
from .trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGeneratorInterface import \
    PokepediaTriviaQuestionGeneratorInterface
from .trivia.triviaRepositories.triviaDatabase import triviaDatabaseQuestionStorage
from .trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import TriviaDatabaseTriviaQuestionRepository
from .trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from .trivia.triviaRepositories.triviaRepository import TriviaRepository
from .trivia.triviaRepositories.willFry.willFryTriviaApiService import WillFryTriviaApiService
from .trivia.triviaRepositories.willFry.willFryTriviaApiServiceInterface import WillFryTriviaApiServiceInterface
from .trivia.triviaRepositories.willFry.willFryTriviaJsonParser import WillFryTriviaJsonParser
from .trivia.triviaRepositories.willFry.willFryTriviaJsonParserInterface import WillFryTriviaJsonParserInterface
from .trivia.triviaRepositories.willFryTriviaQuestionRepository import WillFryTriviaQuestionRepository
from .trivia.triviaRepositories.wwtbamTriviaQuestionRepository import WwtbamTriviaQuestionRepository
from .trivia.triviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from .trivia.triviaVerifier import TriviaVerifier
from .trollmoji.trollmojiHelper import TrollmojiHelper
from .trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmoji.trollmojiSettingsRepository import TrollmojiSettingsRepository
from .trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from .twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from .twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from .twitch.api.twitchApiService import TwitchApiService
from .twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from .twitch.emotes.twitchEmotesHelper import TwitchEmotesHelper
from .twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from .twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from .twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from .twitch.officialAccounts.officialTwitchAccountUserIdProvider import OfficialTwitchAccountUserIdProvider
from .twitch.officialAccounts.officialTwitchAccountUserIdProviderInterface import \
    OfficialTwitchAccountUserIdProviderInterface
from .twitch.subscribers.twitchSubscriptionsRepository import TwitchSubscriptionsRepository
from .twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from .twitch.tokens.twitchTokensRepository import TwitchTokensRepository
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from .twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from .users.userIdsRepository import UserIdsRepository
from .users.userIdsRepositoryInterface import UserIdsRepositoryInterface

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(eventLoop = eventLoop)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = TimberStub()

authRepository = AuthRepository(
    authJsonReader = JsonFileReader(
        eventLoop = eventLoop,
        fileName = '../config/authRepository.json'
    )
)

backingDatabase: BackingDatabase = SqliteBackingDatabase(eventLoop = eventLoop)

networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)

twitchJsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
    timber = timber,
    twitchJsonMapper = twitchJsonMapper
)

twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchCredentialsProvider = authRepository,
    twitchJsonMapper = twitchJsonMapper
)

officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = OfficialTwitchAccountUserIdProvider()

userIdsRepository: Final[UserIdsRepositoryInterface] = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService,
)

twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository,
)

twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface = TwitchSubscriptionsRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository,
)

cutenessRepository: CutenessRepositoryInterface = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository,
)

bannedWordsRepository: Final[BannedWordsRepositoryInterface] = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader(
        eventLoop = eventLoop,
        fileName = 'bannedWords.txt',
    ),
    timber = timber,
)

contentScanner: Final[ContentScannerInterface] = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber,
)

triviaEmoteRepository: TriviaEmoteRepositoryInterface = TriviaEmoteRepository(
    backingDatabase = backingDatabase
)

triviaEmoteGenerator: TriviaEmoteGeneratorInterface = TriviaEmoteGenerator(
    timber = timber,
    triviaEmoteRepository = triviaEmoteRepository
)

triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

triviaSettings: TriviaSettingsInterface = TriviaSettings(
    settingsJsonReader = JsonFileReader(
        eventLoop = eventLoop,
        fileName = 'triviaSettingsRepository.json'
    ),
    triviaSourceParser = triviaSourceParser
)

triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber
)

additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = AdditionalTriviaAnswersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettings = triviaSettings,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository
)

shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaSettings = triviaSettings,
)

toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository,
)

toxicTriviaHelper = ToxicTriviaHelper(
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    timber = timber,
    triviaSettings = triviaSettings,
)

triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)

triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSourceParser = triviaSourceParser,
)

funtoonTokensRepository: FuntoonTokensRepositoryInterface = FuntoonTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    userIdsRepository = userIdsRepository
)

funtoonJsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

funtoonApiService: FuntoonApiServiceInterface = FuntoonApiService(
    funtoonJsonMapper = funtoonJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)

funtoonHelper: FuntoonHelperInterface = FuntoonHelper(
    funtoonApiService = funtoonApiService,
    funtoonJsonMapper = funtoonJsonMapper,
    funtoonTokensRepository = funtoonTokensRepository,
    timber = timber
)

triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettings = triviaSettings,
)

triviaQuestionTypeParser: TriviaQuestionTypeParserInterface = TriviaQuestionTypeParser()

triviaHistoryRepository: TriviaHistoryRepositoryInterface = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaQuestionTypeParser = triviaQuestionTypeParser,
    triviaSettings = triviaSettings,
    triviaSourceParser = triviaSourceParser
)

triviaAnswerChecker: TriviaAnswerCheckerInterface = TriviaAnswerChecker(
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaSettings = triviaSettings,
)

glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = GlacialTriviaQuestionRepository(
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettings = triviaSettings,
    triviaSourceParser = triviaSourceParser,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository,
)

triviaBanHelper: TriviaBanHelperInterface = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonHelper = funtoonHelper,
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    triviaSettings = triviaSettings,
)

triviaScraper: TriviaScraperInterface = TriviaScraper(
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    timber = timber,
    triviaSettings = triviaSettings,
)

triviaDifficultyParser: TriviaDifficultyParserInterface = TriviaDifficultyParser()

millionaireTriviaQuestionStorage: MillionaireTriviaQuestionStorageInterface = MillionaireTriviaQuestionStorage(
    timber = timber
)

openTriviaDatabaseJsonParser: OpenTriviaDatabaseJsonParserInterface = OpenTriviaDatabaseJsonParser(
    timber = timber,
    triviaDifficultyParser = triviaDifficultyParser,
    triviaQuestionTypeParser = triviaQuestionTypeParser
)

openTriviaDatabaseApiService : OpenTriviaDatabaseApiServiceInterface = OpenTriviaDatabaseApiService(
    networkClientProvider = networkClientProvider,
    openTriviaDatabaseJsonParser = openTriviaDatabaseJsonParser,
    timber = timber
)

openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface = OpenTriviaDatabaseSessionTokenRepository(
    backingDatabase = backingDatabase,
    timber = timber
)

openTriviaDatabaseQuestionFetcher: OpenTriviaDatabaseQuestionFetcherInterface = OpenTriviaDatabaseQuestionFetcher(
    openTriviaDatabaseApiService = openTriviaDatabaseApiService,
    openTriviaDatabaseSessionTokenRepository = openTriviaDatabaseSessionTokenRepository,
    timber = timber
)

openTriviaQaQuestionTypeParser: OpenTriviaQaQuestionTypeParserInterface = OpenTriviaQaQuestionTypeParser(
    timber = timber
)
openTriviaQaQuestionStorage: OpenTriviaQaQuestionStorageInterface = OpenTriviaQaQuestionStorage(
    questionTypeParser = openTriviaQaQuestionTypeParser,
    timber = timber
)

pokepediaJsonMapper: PokepediaJsonMapperInterface = PokepediaJsonMapper(
    timber = timber
)

willFryTriviaJsonParser: WillFryTriviaJsonParserInterface = WillFryTriviaJsonParser(
    timber = timber,
    triviaDifficultyParser = triviaDifficultyParser
)

willFryTriviaApiService: WillFryTriviaApiServiceInterface = WillFryTriviaApiService(
    networkClientProvider = networkClientProvider,
    willFryTriviaJsonParser = willFryTriviaJsonParser,
    timber = timber
)

twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = TwitchFriendsUserIdRepository()

trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface = TrollmojiSettingsRepository(
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository
)

twitchEmotesHelper: TwitchEmotesHelperInterface = TwitchEmotesHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchSubscriptionsRepository = twitchSubscriptionsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository,
)

trollmojiHelper: TrollmojiHelperInterface = TrollmojiHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    trollmojiSettingsRepository = trollmojiSettingsRepository,
    twitchEmotesHelper = twitchEmotesHelper
)

triviaTwitchEmoteHelper: TriviaTwitchEmoteHelperInterface = TriviaTwitchEmoteHelper(
    trollmojiHelper = trollmojiHelper
)

pokepediaRepository: PokepediaRepositoryInterface = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    pokepediaJsonMapper = pokepediaJsonMapper,
    timber = timber,
)

pokepediaTriviaQuestionGenerator: PokepediaTriviaQuestionGeneratorInterface = PokepediaTriviaQuestionGenerator(
    pokepediaRepository = pokepediaRepository,
    triviaSettings = triviaSettings,
)

triviaGameMachine = TriviaGameMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    cutenessRepository = cutenessRepository,
    queuedTriviaGameStore = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
    ),
    shinyTriviaHelper = shinyTriviaHelper,
    superTriviaCooldownHelper = SuperTriviaCooldownHelper(
        timeZoneRepository = timeZoneRepository,
        triviaSettings = triviaSettings,
    ),
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    toxicTriviaHelper = toxicTriviaHelper,
    triviaAnswerChecker = triviaAnswerChecker,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameStore = TriviaGameStore(),
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = TriviaRepository(
        backgroundTaskHelper = backgroundTaskHelper,
        bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
            bongoApiService = BongoApiService(
                bongoJsonParser = BongoJsonParser(
                    timber = timber,
                    triviaDifficultyParser = triviaDifficultyParser,
                    triviaQuestionTypeParser = triviaQuestionTypeParser
                ),
                networkClientProvider = networkClientProvider,
                timber = timber,
            ),
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
            additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
            funtoonApiService = funtoonApiService,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
        jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
            additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        lotrTriviaQuestionRepository = None,
        millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
            millionaireTriviaQuestionStorage = millionaireTriviaQuestionStorage,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
            openTriviaDatabaseQuestionFetcher = openTriviaDatabaseQuestionFetcher,
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
            openTriviaQaQuestionStorage = openTriviaQaQuestionStorage,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
            pokepediaTriviaQuestionGenerator = pokepediaTriviaQuestionGenerator,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        quizApiTriviaQuestionRepository = None,
        timber = timber,
        triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
            triviaDatabaseQuestionStorage = triviaDatabaseQuestionStorage.TriviaDatabaseQuestionStorage(
                timber = timber,
                triviaDifficultyParser = triviaDifficultyParser,
                triviaQuestionTypeParser = triviaQuestionTypeParser
            ),
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        triviaQuestionCompanyTriviaQuestionRepository = TriviaQuestionCompanyTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        ),
        triviaQuestionOccurrencesRepository = TriviaQuestionOccurrencesRepository(
            backingDatabase = backingDatabase,
            timber = timber,
        ),
        triviaScraper = triviaScraper,
        triviaSettings = triviaSettings,
        triviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
            timber = timber,
            timeZoneRepository = timeZoneRepository,
        ),
        triviaVerifier = TriviaVerifier(
            timber = timber,
            triviaBanHelper = triviaBanHelper,
            triviaContentScanner = triviaContentScanner,
            triviaHistoryRepository = triviaHistoryRepository
        ),
        twitchHandleProvider = authRepository,
        userIdsRepository = userIdsRepository,
        willFryTriviaQuestionRepository = WillFryTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
            willFryTriviaApiService = willFryTriviaApiService,
        ),
        wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettings = triviaSettings,
        )
    ),
    triviaScoreRepository = TriviaScoreRepository(
        backingDatabase = backingDatabase,
    ),
    triviaSettings = triviaSettings,
    twitchTokensRepository = twitchTokensRepository,
    triviaTwitchEmoteHelper = triviaTwitchEmoteHelper,
    userIdsRepository = userIdsRepository,
)

class ListenerThing(TriviaEventListener):

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        print(f'onNewTriviaEvent(): \"{event}\"')

listenerThing = ListenerThing()
triviaGameMachine.setEventListener(listenerThing)

async def main():
    pass

    await asyncio.sleep(1)

    originalCorrectAnswers: list[str] = [ '$1000000000.559 USD' ]
    correctAnswers = await triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
    compiledCorrectAnswers = await triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

    expandedCompiledCorrectAnswers: set[str] = set()
    for answer in compiledCorrectAnswers:
        expandedCompiledCorrectAnswers.update(await triviaAnswerCompiler.expandNumerals(answer))

    triviaQuestion: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        allWords = None,
        compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
        correctAnswers = correctAnswers,
        originalCorrectAnswers = originalCorrectAnswers,
        category = 'Test Category',
        categoryId = None,
        question = 'In what decade did that one thing happen?',
        triviaId = 'abc123',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = TriviaSource.J_SERVICE,
        triviaSource = TriviaSource.J_SERVICE,
    )

    await triviaScraper.store(triviaQuestion)
    question = await glacialTriviaQuestionRepository.fetchTriviaQuestion(TriviaFetchOptions(
        twitchChannel = 'smCharles',
        twitchChannelId = '74350217',
        questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
    ))

    print(f'({triviaQuestion=}) ({question=})')

    pass
    # await asyncio.sleep(360)

eventLoop.run_until_complete(main())
