import asyncio
from asyncio import AbstractEventLoop

from CynanBot.authRepository import AuthRepository
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.cuteness.cutenessRepository import CutenessRepository
from CynanBot.funtoon.funtoonRepository import FuntoonRepository
from CynanBot.funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from CynanBot.funtoon.funtoonTokensRepository import FuntoonTokensRepository
from CynanBot.funtoon.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.requestsClientProvider import RequestsClientProvider
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.pkmn.pokepediaUtils import PokepediaUtils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBot.trivia.banned.bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from CynanBot.trivia.banned.triviaBanHelper import TriviaBanHelper
from CynanBot.trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from CynanBot.trivia.scraper.triviaScraper import TriviaScraper
from CynanBot.trivia.scraper.triviaScraperInterface import TriviaScraperInterface
from CynanBot.trivia.triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from CynanBot.trivia.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from CynanBot.trivia.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.compilers.triviaQuestionCompiler import \
    TriviaQuestionCompiler
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from CynanBot.trivia.content.triviaContentScanner import TriviaContentScanner
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBot.trivia.games.triviaGameStore import TriviaGameStore
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.score.triviaScoreRepository import TriviaScoreRepository
from CynanBot.trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from CynanBot.trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepository import ToxicTriviaOccurencesRepository
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from CynanBot.trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from CynanBot.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBot.trivia.triviaEventListener import TriviaEventListener
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaGameMachine import TriviaGameMachine
from CynanBot.trivia.triviaHistoryRepository import TriviaHistoryRepository
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBot.trivia.content.triviaContentScanner import TriviaContentScanner
from CynanBot.trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.triviaRepositories.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaRepository import \
    TriviaRepository
from CynanBot.trivia.triviaRepositories.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBot.trivia.triviaVerifier import TriviaVerifier
from CynanBot.twitch.api.twitchApiService import TwitchApiService
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBot.twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepository import UserIdsRepository
from CynanBot.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from CynanBot.twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from CynanBot.twitch.twitchAnonymousUserIdProvider import \
    TwitchAnonymousUserIdProvider
from CynanBot.twitch.twitchAnonymousUserIdProviderInterface import \
    TwitchAnonymousUserIdProviderInterface
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.storage.linesFileReader import LinesFileReader


eventLoop: AbstractEventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(eventLoop = eventLoop)
timber: TimberInterface = Timber(backgroundTaskHelper = backgroundTaskHelper)
authRepository = AuthRepository(
    authJsonReader = JsonFileReader('authRepository.json')
)
backingDatabase: BackingDatabase = BackingSqliteDatabase(eventLoop = eventLoop)
networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)
twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
    timber = timber
)
twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
    twitchCredentialsProvider = authRepository
)
twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface = TwitchAnonymousUserIdProvider()
userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchAnonymousUserIdProvider = twitchAnonymousUserIdProvider,
    twitchApiService = twitchApiService
)
twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService,
)
cutenessRepository = CutenessRepository(
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
                pokepediaUtils = PokepediaUtils(
                    timber = timber
                ),
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

    correctAnswers = await triviaQuestionCompiler.compileResponses([ '$1000000000.559 USD' ])
    cleanedCorrectAnswers = await triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

    expandedCleanedCorrectAnswers: set[str] = set()
    for answer in cleanedCorrectAnswers:
        expandedCleanedCorrectAnswers.update(await triviaAnswerCompiler.expandNumerals(answer))

    triviaQuestion: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers = correctAnswers,
        cleanedCorrectAnswers = list(expandedCleanedCorrectAnswers),
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
