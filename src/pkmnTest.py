import asyncio

from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.requestsClientProvider import RequestsClientProvider
from CynanBot.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository

eventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(eventLoop = eventLoop)
timber: TimberInterface = Timber(backgroundTaskHelper = backgroundTaskHelper)
networkClientProvider: NetworkClientProvider = RequestsClientProvider(timber = timber)

pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
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

    question = await pkmnTriviaQuestionRepository.fetchTriviaQuestion(twitchChannel = 'smCharles')
    print(question)

    pass

eventLoop.run_until_complete(main())
