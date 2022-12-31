import asyncio
from asyncio import AbstractEventLoop

from CynanBotCommon.network.networkClientProvider import NetworkClientProvider
from CynanBotCommon.network.requestsClientProvider import \
    RequestsClientProvider
from CynanBotCommon.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.storage.backingDatabase import BackingDatabase
from CynanBotCommon.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

timber = Timber(
    eventLoop = eventLoop
)

networkClientProvider: NetworkClientProvider = RequestsClientProvider(
    timber = timber
)

pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)

backingDatabase: BackingDatabase = BackingSqliteDatabase(
    eventLoop = eventLoop
)

triviaEmoteGenerator = TriviaEmoteGenerator(
    backingDatabase = backingDatabase,
    timber = timber
)

triviaIdGenerator = TriviaIdGenerator()

triviaSettingsRepository = TriviaSettingsRepository()

pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
    pokepediaRepository = pokepediaRepository,
    timber = timber,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaIdGenerator = triviaIdGenerator,
    triviaSettingsRepository = triviaSettingsRepository
)

async def main():
    pass

    move = await pokepediaRepository.fetchRandomMove(PokepediaGeneration.GENERATION_3)
    print(move)

    question = await pkmnTriviaQuestionRepository.fetchTriviaQuestion(twitchChannel = 'smCharles')
    print(question)

    pass

eventLoop.run_until_complete(main())
