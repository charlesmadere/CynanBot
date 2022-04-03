import asyncio

import aiohttp

from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository


async def doStuff():
    clientSession = aiohttp.ClientSession(
        cookie_jar = aiohttp.DummyCookieJar(),
        timeout = aiohttp.ClientTimeout(total = 5)
    )
    timber = Timber()
    triviaIdGenerator = TriviaIdGenerator()
    triviaSettingsRepository = TriviaSettingsRepository()

    asr = AnalogueStoreRepository(
        clientSession = clientSession,
        timber = timber
    )

    bongo = BongoTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    storeStock = await asr.fetchStoreStock()
    print(storeStock.toStr())

    triviaQuestion = await bongo.fetchTriviaQuestion('smCharles')
    print(triviaQuestion.getResponses())

    await clientSession.close()

asyncio.get_event_loop().run_until_complete(doStuff())
