import asyncio
from asyncio import AbstractEventLoop

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.network.networkClientProvider import NetworkClientProvider
from src.network.requests.requestsClientProvider import RequestsClientProvider
from src.pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from src.pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from src.pkmn.pokepediaRepository import PokepediaRepository
from src.storage.jsonFileReader import JsonFileReader
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.settings.triviaSettings import TriviaSettings
from src.trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from src.trivia.triviaFetchOptions import TriviaFetchOptions
from src.trivia.triviaIdGenerator import TriviaIdGenerator
from src.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from src.trivia.triviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from src.trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGenerator import PokepediaTriviaQuestionGenerator
from src.trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGeneratorInterface import \
    PokepediaTriviaQuestionGeneratorInterface

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

networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)

pokepediaJsonMapper: PokepediaJsonMapperInterface = PokepediaJsonMapper(
    timber = timber
)

pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    pokepediaJsonMapper = pokepediaJsonMapper,
    timber = timber
)

triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

triviaSettings: TriviaSettingsInterface = TriviaSettings(
    settingsJsonReader = JsonFileReader(
        eventLoop = eventLoop,
        fileName = 'triviaSettingsRepository.json',
    ),
    triviaSourceParser = triviaSourceParser,
)

pokepediaTriviaQuestionGenerator: PokepediaTriviaQuestionGeneratorInterface = PokepediaTriviaQuestionGenerator(
    pokepediaRepository = pokepediaRepository,
    triviaSettings = triviaSettings,
)

triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)

pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
    pokepediaTriviaQuestionGenerator = pokepediaTriviaQuestionGenerator,
    triviaIdGenerator = triviaIdGenerator,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettings = triviaSettings,
)

async def main():
    pass

    # mon = await pokepediaRepository.searchPokemon('silvally')
    # print(mon)

    move = await pokepediaRepository.searchMoves('psychic')
    print(move)

    # blah = PokepediaDamageClass.getTypeBasedDamageClass(PokepediaElementType.BUG)
    # print(blah)

    # fetchOptions = TriviaFetchOptions(
    #     twitchChannel = 'smCharles',
    #     twitchChannelId = '12345'
    # )

    # question = await pkmnTriviaQuestionRepository.fetchTriviaQuestion(fetchOptions = fetchOptions)
    # print(question)

    pass

eventLoop.run_until_complete(main())
