import asyncio
from asyncio import AbstractEventLoop

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.network.aioHttpClientProvider import AioHttpClientProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.tempFileHelper.ttsTempFileHelper import TtsTempFileHelper
from src.tts.tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from src.tts.ttsMonster.ttsMonsterFileManager import TtsMonsterFileManager
from src.tts.ttsMonster.ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from src.ttsMonster.apiService.ttsMonsterApiService import TtsMonsterApiService
from src.ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from src.ttsMonster.mapper.ttsMonsterJsonMapper import TtsMonsterJsonMapper
from src.ttsMonster.mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

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

ttsTempFileHelper: TtsTempFileHelperInterface = TtsTempFileHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

ttsMonsterFileManager: TtsMonsterFileManagerInterface = TtsMonsterFileManager(
    eventLoop = eventLoop,
    timber = timber,
    ttsMonsterApiService = ttsMonsterApiService,
    ttsTempFileHelper = ttsTempFileHelper
)

async def main():
    pass

    files = await ttsMonsterFileManager.saveTtsUrlsToNewFiles([
        'https://script-samples.tts.monster/Alpha.wav',
        'https://script-samples.tts.monster/Stella.wav',
        'https://script-samples.tts.monster/Leader.wav'
    ])

    print(f'{files=}')

    # response = await ttsMonsterApiService.fetchGeneratedTts(
    #     ttsUrl = 'https://script-samples.tts.monster/Alpha.wav'
    # )
    #
    #
    #
    # async with aiofiles.open(
    #     file = 'ttsMonsterTest.wav',
    #     mode = 'wb'
    # ) as file:
    #     await file.write(response)
    #     await file.flush()

    pass

eventLoop.run_until_complete(main())
