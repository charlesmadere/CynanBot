import asyncio
from asyncio import AbstractEventLoop

from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc.backgroundTaskHelper import BackgroundTaskHelper
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .network.networkClientProvider import NetworkClientProvider
from .network.requests.requestsClientProvider import RequestsClientProvider
from .pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from .pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from .pkmn.pokepediaRepository import PokepediaRepository
from .storage.jsonFileReader import JsonFileReader
from .timber.timber import Timber
from .timber.timberInterface import TimberInterface
from .trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from .trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from .trivia.misc.triviaSourceParser import TriviaSourceParser
from .trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from .trivia.settings.triviaSettings import TriviaSettings
from .trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from .trivia.triviaFetchOptions import TriviaFetchOptions
from .trivia.triviaIdGenerator import TriviaIdGenerator
from .trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .trivia.triviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from .trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGenerator import PokepediaTriviaQuestionGenerator
from .trivia.triviaRepositories.pokepedia.pokepediaTriviaQuestionGeneratorInterface import \
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

    move = await pokepediaRepository.searchMoves('thunderbolt')
    print(move)

    # blah = PokepediaDamageClass.getTypeBasedDamageClass(PokepediaElementType.BUG)
    # print(blah)

    fetchOptions = TriviaFetchOptions(
        twitchChannel = 'smCharles',
        twitchChannelId = '12345'
    )

    question = await pkmnTriviaQuestionRepository.fetchTriviaQuestion(fetchOptions = fetchOptions)
    print(question)

    pass

eventLoop.run_until_complete(main())
