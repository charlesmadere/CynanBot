import asyncio
from asyncio import AbstractEventLoop

from location.timeZoneRepository import TimeZoneRepository
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from misc.backgroundTaskHelper import BackgroundTaskHelper
from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from network.networkClientProvider import NetworkClientProvider
from network.requestsClientProvider import RequestsClientProvider
from pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from pkmn.pokepediaRepository import PokepediaRepository
from storage.jsonFileReader import JsonFileReader
from timber.timber import Timber
from timber.timberInterface import TimberInterface
from trivia.triviaFetchOptions import TriviaFetchOptions
from trivia.triviaIdGenerator import TriviaIdGenerator
from trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from trivia.triviaSettingsRepository import TriviaSettingsRepository

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

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

triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

triviaSettingsRepository = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)

pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
    pokepediaRepository = pokepediaRepository,
    timber = timber,
    triviaIdGenerator = triviaIdGenerator,
    triviaSettingsRepository = triviaSettingsRepository
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
