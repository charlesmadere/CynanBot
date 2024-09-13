import asyncio
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os

from src.network.aioHttpClientProvider import AioHttpClientProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.ttsMonster.apiService.ttsMonsterApiService import TtsMonsterApiService
from src.ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from src.ttsMonster.mapper.ttsMonsterJsonMapper import TtsMonsterJsonMapper
from src.ttsMonster.mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface

# https://script-samples.tts.monster/Alpha.wav

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

timber: TimberInterface = TimberStub()

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    timber = timber
)

ttsMonsterWebsiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface = TtsMonsterWebsiteVoiceMapper()

ttsMonsterJsonMapper: TtsMonsterJsonMapperInterface = TtsMonsterJsonMapper(
    timber = timber,
    websiteVoiceMapper = ttsMonsterWebsiteVoiceMapper
)

ttsMonsterApiService: TtsMonsterApiServiceInterface = TtsMonsterApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    ttsMonsterJsonMapper = ttsMonsterJsonMapper
)

async def main():
    response = await ttsMonsterApiService.fetchGeneratedTts(
        ttsUrl = 'https://script-samples.tts.monster/Alpha.wav'
    )

    async with aiofiles.open(
        file = 'ttsMonsterTest.wav',
        mode = 'wb'
    ) as file:
        await file.write(response)
        await file.flush()

    pass

eventLoop.run_until_complete(main())
