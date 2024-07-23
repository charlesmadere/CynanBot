import asyncio
import locale
import time
from asyncio import AbstractEventLoop, InvalidStateError
from requests import get
from rich.console import Console
from rich.table import Table

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.authRepository import AuthRepository
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.misc.generalSettingsRepository import GeneralSettingsRepository
from src.network.aioHttpClientProvider import AioHttpClientProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.network.networkClientType import NetworkClientType
from src.network.networkJsonMapper import NetworkJsonMapper
from src.network.networkJsonMapperInterface import NetworkJsonMapperInterface
from src.network.requestsClientProvider import RequestsClientProvider
from src.storage.databaseType import DatabaseType
from src.storage.backingDatabase import BackingDatabase
from src.storage.backingPsqlDatabase import BackingPsqlDatabase
from src.storage.backingSqliteDatabase import BackingSqliteDatabase
from src.storage.jsonFileReader import JsonFileReader
from src.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.trivia.additionalAnswers.additionalTriviaAnswersRepository import AdditionalTriviaAnswersRepository
from src.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from src.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from src.trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from src.trivia.triviaFetchOptions import TriviaFetchOptions
from src.trivia.triviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from src.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from src.trivia.triviaSettingsRepository import TriviaSettingsRepository
from src.trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from src.twitch.api.twitchApiService import TwitchApiService
from src.twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.twitchAnonymousUserIdProvider import TwitchAnonymousUserIdProvider
from src.twitch.twitchAnonymousUserIdProviderInterface import TwitchAnonymousUserIdProviderInterface
from src.twitch.twitchTokensRepository import TwitchTokensRepository
from src.twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from src.users.userIdsRepository import UserIdsRepository
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository
)

triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)

triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)

triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)

authRepository = AuthRepository(
    authJsonReader = JsonFileReader('authRepository.json')
)

networkJsonMapper: NetworkJsonMapperInterface = NetworkJsonMapper()
storageJsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('generalSettingsRepository.json'),
    networkJsonMapper = networkJsonMapper,
    storageJsonMapper = storageJsonMapper
)

generalSettingsSnapshot = generalSettingsRepository.getAll()

backingDatabase: BackingDatabase
match generalSettingsSnapshot.requireDatabaseType():
    case DatabaseType.POSTGRESQL:
        backingDatabase = BackingPsqlDatabase(
            eventLoop = eventLoop,
            psqlCredentialsProvider = PsqlCredentialsProvider(
                credentialsJsonReader = JsonFileReader('psqlCredentials.json')
            ),
            timber = timber
        )

    case DatabaseType.SQLITE:
        backingDatabase = BackingSqliteDatabase(
            eventLoop = eventLoop
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured DatabaseType: \"{generalSettingsSnapshot.requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider
match generalSettingsSnapshot.requireNetworkClientType():
    case NetworkClientType.AIOHTTP:
        networkClientProvider = AioHttpClientProvider(
            eventLoop = eventLoop,
            timber = timber
        )

    case NetworkClientType.REQUESTS:
        networkClientProvider = RequestsClientProvider(
            timber = timber
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured NetworkClientType: \"{generalSettingsSnapshot.requireNetworkClientType()}\"')

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
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
)

twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface = TwitchAnonymousUserIdProvider()

userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchAnonymousUserIdProvider = twitchAnonymousUserIdProvider,
    twitchApiService = twitchApiService
)

twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('twitchTokensRepositorySeedFile.json')
)

additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = AdditionalTriviaAnswersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = GlacialTriviaQuestionRepository(
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository
)

triviaFetchOptions = TriviaFetchOptions(twitchChannel="", twitchChannelId="")

table = Table(title="Glacial Questions")

questions = None

tries = 0

questionRetrievalTask = eventLoop.create_task(glacialTriviaQuestionRepository.fetchAllQuestionAnswerTriviaQuestions(fetchOptions=triviaFetchOptions))

questions = eventLoop.run_until_complete(questionRetrievalTask)

columns = ["Question", "Correct Answers", "Possible Optional Answer Words", "Trivia Type"]

for column in columns:
    table.add_column(column)
if questions is not None:
    for question in questions:
        questionWords = question.question.split(' ')
        optionals = []
        for questionWord in questionWords:
            for questionAnswer in question.cleanedCorrectAnswers:
                for splitQuestionAnswer in questionAnswer.split(' '):
                    if questionWord.capitalize() == splitQuestionAnswer.capitalize():
                        if splitQuestionAnswer not in optionals:
                            optionals.append(splitQuestionAnswer)

        if len(optionals) > 0:
            row = [question.question, ', '.join(question.cleanedCorrectAnswers), ', '.join(optionals), question.triviaType.name]
            table.add_row(*row, style='bright_green')

console = Console()
console.print(table)