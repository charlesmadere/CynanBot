import asyncio
from asyncio import AbstractEventLoop

from contentScanner.bannedWordsRepository import BannedWordsRepository
from contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from contentScanner.contentScanner import ContentScanner
from contentScanner.contentScannerInterface import ContentScannerInterface
from cuteness.cutenessRepository import CutenessRepository
from cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from funtoon.funtoonRepository import FuntoonRepository
from funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from funtoon.funtoonTokensRepository import FuntoonTokensRepository
from funtoon.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from location.timeZoneRepository import TimeZoneRepository
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from misc.authRepository import AuthRepository
from misc.backgroundTaskHelper import BackgroundTaskHelper
from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from network.networkClientProvider import NetworkClientProvider
from network.requestsClientProvider import RequestsClientProvider
from pkmn.pokepediaRepository import PokepediaRepository
from storage.backingDatabase import BackingDatabase
from storage.backingSqliteDatabase import BackingSqliteDatabase
from storage.jsonFileReader import JsonFileReader
from storage.linesFileReader import LinesFileReader
from timber.timber import Timber
from timber.timberInterface import TimberInterface
from trivia.additionalAnswers.additionalTriviaAnswersRepository import AdditionalTriviaAnswersRepository
from trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from trivia.banned.bannedTriviaIdsRepository import BannedTriviaIdsRepository
from trivia.banned.bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from trivia.banned.triviaBanHelper import TriviaBanHelper
from trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from trivia.content.triviaContentScanner import TriviaContentScanner
from trivia.content.triviaContentScannerInterface import TriviaContentScannerInterface
from trivia.emotes.triviaEmoteGenerator import TriviaEmoteGenerator
from trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from trivia.events.absTriviaEvent import AbsTriviaEvent
from trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from trivia.games.triviaGameStore import TriviaGameStore
from trivia.questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from trivia.questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from trivia.questions.triviaSource import TriviaSource
from trivia.score.triviaScoreRepository import TriviaScoreRepository
from trivia.scraper.triviaScraper import TriviaScraper
from trivia.scraper.triviaScraperInterface import TriviaScraperInterface
from trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from trivia.specialStatus.shinyTriviaOccurencesRepository import ShinyTriviaOccurencesRepository
from trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from trivia.specialStatus.toxicTriviaOccurencesRepository import ToxicTriviaOccurencesRepository
from trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from trivia.triviaAnswerChecker import TriviaAnswerChecker
from trivia.triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from trivia.triviaDifficulty import TriviaDifficulty
from trivia.triviaEventListener import TriviaEventListener
from trivia.triviaFetchOptions import TriviaFetchOptions
from trivia.triviaGameMachine import TriviaGameMachine
from trivia.triviaHistoryRepository import TriviaHistoryRepository
from trivia.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from trivia.triviaIdGenerator import TriviaIdGenerator
from trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from trivia.triviaRepositories.bongoTriviaQuestionRepository import BongoTriviaQuestionRepository
from trivia.triviaRepositories.funtoonTriviaQuestionRepository import FuntoonTriviaQuestionRepository
from trivia.triviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from trivia.triviaRepositories.jServiceTriviaQuestionRepository import JServiceTriviaQuestionRepository
from trivia.triviaRepositories.millionaireTriviaQuestionRepository import MillionaireTriviaQuestionRepository
from trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import OpenTriviaQaTriviaQuestionRepository
from trivia.triviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import TriviaDatabaseTriviaQuestionRepository
from trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from trivia.triviaRepositories.triviaRepository import TriviaRepository
from trivia.triviaRepositories.willFryTriviaQuestionRepository import WillFryTriviaQuestionRepository
from trivia.triviaRepositories.wwtbamTriviaQuestionRepository import WwtbamTriviaQuestionRepository
from trivia.triviaSettingsRepository import TriviaSettingsRepository
from trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from trivia.triviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from trivia.triviaVerifier import TriviaVerifier
from twitch.api.twitchApiService import TwitchApiService
from twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from twitch.api.twitchJsonMapper import TwitchJsonMapper
from twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from twitch.officialTwitchAccountUserIdProvider import OfficialTwitchAccountUserIdProvider
from twitch.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from twitch.twitchTokensRepository import TwitchTokensRepository
from twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from users.userIdsRepository import UserIdsRepository
from users.userIdsRepositoryInterface import UserIdsRepositoryInterface

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(eventLoop = eventLoop)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository
)

authRepository = AuthRepository(
    authJsonReader = JsonFileReader('authRepository.json')
)

backingDatabase: BackingDatabase = BackingSqliteDatabase(eventLoop = eventLoop)

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
    twitchJsonMapper = twitchJsonMapper,
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper
)

officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = OfficialTwitchAccountUserIdProvider()

userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    officialTwitchAccountUserIdProvider = officialTwitchAccountUserIdProvider,
    timber = timber,
    twitchApiService = twitchApiService
)

twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository
)

cutenessRepository: CutenessRepositoryInterface = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader('bannedWords.txt'),
    timber = timber
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber
)

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader('bannedWords.txt'),
    timber = timber
)

triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber
)
triviaEmoteGenerator: TriviaEmoteGeneratorInterface = TriviaEmoteGenerator(
    backingDatabase = backingDatabase,
    timber = timber
)
triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)
additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = AdditionalTriviaAnswersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
toxicTriviaHelper = ToxicTriviaHelper(
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)
triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()
bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber
)
funtoonTokensRepository: FuntoonTokensRepositoryInterface = FuntoonTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber
)
funtoonRepository: FuntoonRepositoryInterface = FuntoonRepository(
    funtoonTokensRepository = funtoonTokensRepository,
    networkClientProvider = networkClientProvider,
    timber = timber
)
triviaBanHelper: TriviaBanHelperInterface = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonRepository = funtoonRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaHistoryRepository: TriviaHistoryRepositoryInterface = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaAnswerChecker: TriviaAnswerCheckerInterface = TriviaAnswerChecker(
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaSettingsRepository = triviaSettingsRepository
)
glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = GlacialTriviaQuestionRepository(
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository
)
triviaScraper: TriviaScraperInterface = TriviaScraper(
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaGameMachine = TriviaGameMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    cutenessRepository = cutenessRepository,
    queuedTriviaGameStore = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    shinyTriviaHelper = shinyTriviaHelper,
    superTriviaCooldownHelper = SuperTriviaCooldownHelper(
        triviaSettingsRepository = triviaSettingsRepository
    ),
    timber = timber,
    toxicTriviaHelper = toxicTriviaHelper,
    triviaAnswerChecker = triviaAnswerChecker,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameStore = TriviaGameStore(),
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = TriviaRepository(
        backgroundTaskHelper = backgroundTaskHelper,
        bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
            additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
        jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
            additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        lotrTriviaQuestionRepository = None,
        millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
            backingDatabase = backingDatabase,
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
            pokepediaRepository = PokepediaRepository(
                networkClientProvider = networkClientProvider,
                timber = timber
            ),
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        quizApiTriviaQuestionRepository = None,
        timber = timber,
        triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        triviaQuestionCompanyTriviaQuestionRepository = TriviaQuestionCompanyTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        triviaScraper = triviaScraper,
        triviaSettingsRepository = triviaSettingsRepository,
        triviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
            timber = timber
        ),
        triviaVerifier = TriviaVerifier(
            timber = timber,
            triviaBanHelper = triviaBanHelper,
            triviaContentScanner = triviaContentScanner,
            triviaHistoryRepository = triviaHistoryRepository
        ),
        twitchHandleProvider = authRepository,
        willFryTriviaQuestionRepository = WillFryTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        )
    ),
    triviaScoreRepository = TriviaScoreRepository(
        backingDatabase = backingDatabase
    ),
    triviaSettingsRepository = triviaSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
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
        triviaSource = TriviaSource.J_SERVICE,
    )

    await triviaScraper.store(triviaQuestion)
    question = await glacialTriviaQuestionRepository.fetchTriviaQuestion(TriviaFetchOptions(
        twitchChannel = 'smCharles',
        questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
    ))

    print(f'({triviaQuestion=}) ({question=})')

    pass
    # await asyncio.sleep(360)

eventLoop.run_until_complete(main())
