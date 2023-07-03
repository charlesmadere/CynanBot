import asyncio

from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.network.networkClientProvider import NetworkClientProvider
from CynanBotCommon.network.requestsClientProvider import \
    RequestsClientProvider
from CynanBotCommon.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBotCommon.pkmn.pokepediaElementType import PokepediaElementType
from CynanBotCommon.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.storage.jsonFileReader import JsonFileReader
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository

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
    settingsJsonReader = JsonFileReader('CynanBotCommon/trivia/triviaSettingsRepository.json')
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
