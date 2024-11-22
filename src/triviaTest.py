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
from src.funtoon.funtoonApiService import FuntoonApiService
from src.funtoon.funtoonApiServiceInterface import FuntoonApiServiceInterface
from src.funtoon.funtoonApiService import FuntoonApiService
from src.funtoon.funtoonJsonMapper import FuntoonJsonMapper
from src.pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from src.trollmoji.trollmojiSettingsRepository import TrollmojiSettingsRepository
from .twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from .twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from .twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from .twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from .trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from src.twitch.emotes.twitchEmotesHelper import TwitchEmotesHelper
from .trollmoji.trollmojiHelper import TrollmojiHelper
from .trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from .trivia.emotes.twitch.triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from src.trivia.triviaRepositories.willFry.willFryTriviaApiService import WillFryTriviaApiService
from src.trivia.triviaRepositories.willFry.willFryTriviaJsonParser import WillFryTriviaJsonParser
from .trivia.triviaRepositories.willFry.willFryTriviaJsonParserInterface import WillFryTriviaJsonParserInterface
from .trivia.triviaRepositories.willFry.willFryTriviaApiServiceInterface import WillFryTriviaApiServiceInterface
from .pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from src.trivia.emotes.twitch.triviaTwitchEmoteHelper import TriviaTwitchEmoteHelper
from src.trivia.misc.triviaDifficultyParser import TriviaDifficultyParser
from src.trivia.misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from src.trivia.misc.triviaQuestionTypeParser import TriviaQuestionTypeParser
from src.trivia.misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from src.trivia.triviaRepositories import pokepedia
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParserInterface import OpenTriviaQaQuestionTypeParserInterface
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParser import OpenTriviaQaQuestionTypeParser
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionStorage import OpenTriviaQaQuestionStorage
from .trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionStorageInterface import OpenTriviaQaQuestionStorageInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepository import OpenTriviaDatabaseSessionTokenRepository
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import OpenTriviaDatabaseSessionTokenRepositoryInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseQuestionFetcherInterface import OpenTriviaDatabaseQuestionFetcherInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParser import OpenTriviaDatabaseJsonParser
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParserInterface import OpenTriviaDatabaseJsonParserInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseApiService import OpenTriviaDatabaseApiService
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseApiServiceInterface import OpenTriviaDatabaseApiServiceInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseQuestionFetcher import OpenTriviaDatabaseQuestionFetcher
from .trivia.triviaRepositories.millionaire.millionaireTriviaQuestionStorage import MillionaireTriviaQuestionStorage
from .trivia.triviaRepositories.millionaire.millionaireTriviaQuestionStorageInterface import MillionaireTriviaQuestionStorageInterface
from .trivia.triviaRepositories.bongo.bongoJsonParser import BongoJsonParser
from .trivia.triviaRepositories.bongo.bongoApiService import BongoApiService
from src.trivia.triviaRepositories.triviaDatabase import triviaDatabaseQuestionStorage
from .funtoon.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from src.trivia.emotes.triviaEmoteRepository import TriviaEmoteRepository
from src.trivia.emotes.triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
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

triviaEmoteRepository: TriviaEmoteRepositoryInterface = TriviaEmoteRepository(
    backingDatabase = backingDatabase
)

triviaEmoteGenerator: TriviaEmoteGeneratorInterface = TriviaEmoteGenerator(
    timber = timber,
    triviaEmoteRepository = triviaEmoteRepository
)
triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)
triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
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
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository 
)
shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository
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
    timber = timber,
    userIdsRepository = userIdsRepository
)

funtoonJsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

funtoonApiService: FuntoonApiServiceInterface = FuntoonApiService(
    funtoonJsonMapper = funtoonJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)
funtoonRepository: FuntoonRepositoryInterface = FuntoonRepository(
    funtoonApiService = funtoonApiService,
    funtoonJsonMapper = funtoonJsonMapper,
    funtoonTokensRepository = funtoonTokensRepository,
    timber = timber
)
triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)

triviaQuestionTypeParser: TriviaQuestionTypeParserInterface = TriviaQuestionTypeParser()

triviaHistoryRepository: TriviaHistoryRepositoryInterface = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaQuestionTypeParser = triviaQuestionTypeParser,
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
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository
)
triviaBanHelper: TriviaBanHelperInterface = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonRepository = funtoonRepository,
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScraper: TriviaScraperInterface = TriviaScraper(
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
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
    timber=timber,
    twitchApiService=twitchApiService,
    twitchHandleProvider=authRepository,
    twitchTokensRepository=twitchTokensRepository,
    userIdsRepository=userIdsRepository

)
trollmojiHelper: TrollmojiHelperInterface = TrollmojiHelper(
    timber= timber,
    timeZoneRepository=timeZoneRepository,
    trollmojiSettingsRepository=trollmojiSettingsRepository,
    twitchEmotesHelper=twitchEmotesHelper
)
triviaTwitchEmoteHelper: TriviaTwitchEmoteHelperInterface = TriviaTwitchEmoteHelper(
    trollmojiHelper = trollmojiHelper
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
        timeZoneRepository = timeZoneRepository,
        triviaSettingsRepository = triviaSettingsRepository
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
                networkClientProvider = networkClientProvider,
                bongoJsonParser = BongoJsonParser(
                    timber = timber,
                    triviaDifficultyParser = triviaDifficultyParser,
                    triviaQuestionTypeParser = triviaQuestionTypeParser
                ),
                timber = timber
            ),
            timber = timber,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
            additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
            funtoonApiService = funtoonApiService,
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
            millionaireTriviaQuestionStorage = millionaireTriviaQuestionStorage,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
            openTriviaDatabaseQuestionFetcher = openTriviaDatabaseQuestionFetcher,
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaQuestionTypeParser = triviaQuestionTypeParser,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
            openTriviaQaQuestionStorage = openTriviaQaQuestionStorage,
            triviaQuestionCompiler = triviaQuestionCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
            pokepediaRepository = PokepediaRepository(
                networkClientProvider = networkClientProvider,
                pokepediaJsonMapper = pokepediaJsonMapper,
                timber = timber
            ),
            timber = timber,
            triviaIdGenerator = triviaIdGenerator,
            triviaSettingsRepository = triviaSettingsRepository
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
            timber = timber,
            timeZoneRepository = timeZoneRepository
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
            triviaSettingsRepository = triviaSettingsRepository,
            willFryTriviaApiService = willFryTriviaApiService
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
    triviaTwitchEmoteHelper = triviaTwitchEmoteHelper,
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
