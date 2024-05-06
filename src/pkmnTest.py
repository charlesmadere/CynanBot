import asyncio
from asyncio import AbstractEventLoop

from CynanBot.misc.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.requestsClientProvider import RequestsClientProvider
from CynanBot.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.pkmn.pokepediaUtils import PokepediaUtils
from CynanBot.pkmn.pokepediaUtilsInterface import PokepediaUtilsInterface
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper
)

networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)

pokepediaUtils: PokepediaUtilsInterface = PokepediaUtils(
    timber = timber
)

pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    pokepediaUtils = pokepediaUtils,
    timber = timber
)

triviaIdGenerator = TriviaIdGenerator()
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

    # move = await pokepediaRepository.searchMoves('multi-attack')
    # print(move)

    blah = PokepediaDamageClass.getTypeBasedDamageClass(PokepediaElementType.BUG)
    print(blah)

    fetchOptions = TriviaFetchOptions(
        twitchChannel = 'smCharles',
        twitchChannelId = '12345'
    )

    question = await pkmnTriviaQuestionRepository.fetchTriviaQuestion(fetchOptions = fetchOptions)
    print(question)

    pass

eventLoop.run_until_complete(main())
