import asyncio
from datetime import timedelta

from CynanBot.authRepository import AuthRepository
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.cuteness.cutenessRepository import CutenessRepository
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.requestsClientProvider import RequestsClientProvider
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from CynanBot.trivia.banned.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBot.trivia.games.triviaGameStore import TriviaGameStore
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.shinyTriviaHelper import ShinyTriviaHelper
from CynanBot.trivia.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBot.trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from CynanBot.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBot.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.triviaContentScanner import TriviaContentScanner
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBot.trivia.triviaEventListener import TriviaEventListener
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaGameMachine import TriviaGameMachine
from CynanBot.trivia.triviaHistoryRepository import TriviaHistoryRepository
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBot.trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
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
from CynanBot.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBot.trivia.triviaVerifier import TriviaVerifier
from CynanBot.twitch.api.twitchApiService import TwitchApiService
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.users.userIdsRepository import UserIdsRepository

eventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(eventLoop = eventLoop)
timber: TimberInterface = Timber(backgroundTaskHelper = backgroundTaskHelper)
authRepository = AuthRepository()
backingDatabase: BackingDatabase = BackingSqliteDatabase(eventLoop = eventLoop)
networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)
twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    twitchCredentialsProvider = authRepository
)
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    timber = timber
)
triviaAnswerCompiler = TriviaAnswerCompiler(
    timber = timber
)
triviaEmoteGenerator = TriviaEmoteGenerator(
    backingDatabase = backingDatabase,
    timber = timber
)
triviaSettingsRepository = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)
additionalTriviaAnswersRepository = AdditionalTriviaAnswersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
shinyTriviaOccurencesRepository = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaQuestionCompiler = TriviaQuestionCompiler()
triviaIdGenerator = TriviaIdGenerator()
bannedTriviaIdsRepository = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaHistoryRepository = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaAnswerChecker = TriviaAnswerChecker(
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaGameMachine = TriviaGameMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    cutenessRepository = cutenessRepository,
    queuedTriviaGameStore = QueuedTriviaGameStore(
        timber = timber,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    shinyTriviaHelper = shinyTriviaHelper,
    superTriviaCooldownHelper = SuperTriviaCooldownHelper(
        triviaSettingsRepository = triviaSettingsRepository
    ),
    timber = timber,
    triviaAnswerChecker = triviaAnswerChecker,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameStore = TriviaGameStore(),
    triviaRepository = TriviaRepository(
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
        jokeTriviaQuestionRepository = None,
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
        triviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
            timber = timber
        ),
        triviaSettingsRepository = triviaSettingsRepository,
        triviaVerifier = TriviaVerifier(
            bannedTriviaIdsRepository = bannedTriviaIdsRepository,
            timber = timber,
            triviaContentScanner = triviaContentScanner,
            triviaHistoryRepository = triviaHistoryRepository
        ),
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
    )
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

    triviaQuestion: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers=correctAnswers,
        cleanedCorrectAnswers=cleanedCorrectAnswers,
        category='Test Category',
        categoryId=None,
        question='In what decade did that one thing happen?',
        triviaId='abc123',
        triviaDifficulty=TriviaDifficulty.UNKNOWN,
        triviaSource=TriviaSource.J_SERVICE,
    )

    result = await triviaAnswerChecker.checkAnswer(
        answer = 'friends',
        triviaQuestion = triviaQuestion
    )

    print(f'triviaQuestion={triviaQuestion}\nresult={result}')

    pass
    # await asyncio.sleep(360)

eventLoop.run_until_complete(main())
