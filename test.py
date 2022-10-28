import asyncio
from datetime import timedelta

from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.networkClientProvider import NetworkClientProvider
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBotCommon.trivia.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBotCommon.trivia.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBotCommon.trivia.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBotCommon.trivia.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBotCommon.trivia.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBotCommon.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBotCommon.trivia.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBotCommon.trivia.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBotCommon.trivia.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBotCommon.trivia.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBotCommon.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaContentScanner import TriviaContentScanner
from CynanBotCommon.trivia.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.triviaDifficulty import TriviaDifficulty
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaErrorDict import TriviaErrorDict
from CynanBotCommon.trivia.triviaEventListener import TriviaEventListener
from CynanBotCommon.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaGameStore import TriviaGameStore
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.trivia.triviaSource import TriviaSource
from CynanBotCommon.trivia.triviaVerifier import TriviaVerifier
from CynanBotCommon.trivia.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBotCommon.trivia.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository

eventLoop = asyncio.get_event_loop()
backingDatabase = BackingDatabase()
networkClientProvider = NetworkClientProvider(eventLoop = eventLoop)
timber = Timber(eventLoop = eventLoop)
triviaAnswerCompiler = TriviaAnswerCompiler()
triviaEmoteGenerator = TriviaEmoteGenerator(backingDatabase)
triviaQuestionCompiler = TriviaQuestionCompiler()
triviaIdGenerator = TriviaIdGenerator()
triviaSettingsRepository = TriviaSettingsRepository()
bannedTriviaIdsRepository = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner = TriviaContentScanner(
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
triviaEmoteGenerator = TriviaEmoteGenerator(backingDatabase)

triviaGameMachine = TriviaGameMachine(
    eventLoop = eventLoop,
    queuedTriviaGameStore = QueuedTriviaGameStore(
        timber = timber,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    timber = timber,
    triviaAnswerChecker = triviaAnswerChecker,
    triviaGameStore = TriviaGameStore(),
    triviaRepository = TriviaRepository(
        bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        jokeTriviaQuestionRepository = None,
        jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        lotrTriviaQuestionRepository = None,
        millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
            networkClientProvider = networkClientProvider,
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        quizApiTriviaQuestionRepository = None,
        timber = timber,
        triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        triviaSourceInstabilityDict = TriviaErrorDict(),
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
            triviaEmoteGenerator = triviaEmoteGenerator,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
            timber = timber,
            triviaEmoteGenerator = triviaEmoteGenerator,
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

    # triviaGameMachine.submitAction(StartNewSuperTriviaGameAction(
    #     isQueueActionConsumed = False,
    #     numberOfGames = 1,
    #     perUserAttempts = 2,
    #     pointsForWinning = 25,
    #     pointsMultiplier = 5,
    #     secondsToLive = 5,
    #     twitchChannel = 'smCharles',
    #     triviaFetchOptions = TriviaFetchOptions(
    #         twitchChannel = 'smCharles',
    #         isJokeTriviaRepositoryEnabled = False,
    #         questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
    #     )
    # ))

    # await asyncio.sleep(0.75)

    # triviaGameMachine.submitAction(StartNewSuperTriviaGameAction(
    #     isQueueActionConsumed = False,
    #     numberOfGames = 1,
    #     perUserAttempts = 2,
    #     pointsForWinning = 25,
    #     pointsMultiplier = 5,
    #     secondsToLive = 5,
    #     twitchChannel = 'smCharles',
    #     triviaFetchOptions = TriviaFetchOptions(
    #         twitchChannel = 'smCharles',
    #         isJokeTriviaRepositoryEnabled = False,
    #         questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
    #     )
    # ))

    correctAnswer = 'the 1950s'
    triviaQuestion: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers=[correctAnswer],
        cleanedCorrectAnswers=await triviaAnswerCompiler.expandNumerals(correctAnswer)
        ,
        category='Test Category',
        categoryId=None,
        emote = '🏫',
        question='In what decade did that one thing happen?',
        triviaId='abc123',
        triviaDifficulty=TriviaDifficulty.UNKNOWN,
        triviaSource=TriviaSource.J_SERVICE,
    )

    result = await triviaAnswerChecker.checkAnswer(
        answer = '1950s',
        triviaQuestion = triviaQuestion,
        extras = None
    )

    print(f'triviaQuestion={triviaQuestion}\nresult={result}')

    pass
    # await asyncio.sleep(360)

eventLoop.run_until_complete(main())
