import asyncio
from asyncio import AbstractEventLoop

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsMonster.ttsMonsterFileManager import TtsMonsterFileManager
from src.tts.ttsMonster.ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from src.ttsMonster.apiService.ttsMonsterApiService import TtsMonsterApiService
from src.ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from src.ttsMonster.apiService.ttsMonsterPrivateApiService import TtsMonsterPrivateApiService
from src.ttsMonster.apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from src.ttsMonster.helper.ttsMonsterPrivateApiHelper import TtsMonsterPrivateApiHelper
from src.ttsMonster.helper.ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from src.ttsMonster.mapper.ttsMonsterJsonMapper import TtsMonsterJsonMapper
from src.ttsMonster.mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

class FakeTtsMonsterKeyAndUserIdRepository(TtsMonsterKeyAndUserIdRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(self, twitchChannel: str) -> TtsMonsterKeyAndUserId | None:
        raise RuntimeError('Not implemented')

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber
)

twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = TwitchFriendsUserIdRepository()

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

ttsMonsterFileManager: TtsMonsterFileManagerInterface = TtsMonsterFileManager(
    eventLoop = eventLoop,
    timber = timber,
    ttsMonsterApiService = ttsMonsterApiService
)

ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface = FakeTtsMonsterKeyAndUserIdRepository()

ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper()

ttsMonsterPrivateApiService: TtsMonsterPrivateApiServiceInterface = TtsMonsterPrivateApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
)

ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface = TtsMonsterPrivateApiHelper(
    timber = timber,
    ttsMonsterKeyAndUserIdRepository = ttsMonsterKeyAndUserIdRepository,
    ttsMonsterPrivateApiService = ttsMonsterPrivateApiService
)

async def main():
    pass

    fileUrls: list[str] = [
        'https://script-samples.tts.monster/Alpha.wav',
        'https://script-samples.tts.monster/Stella.wav',
        'https://script-samples.tts.monster/Leader.wav'
    ]

    charlesUserId = await twitchFriendsUserIdRepository.getCharlesUserId()

    if charlesUserId is not None:
        ttsMonsterUrls = await ttsMonsterPrivateApiHelper.generateTts(
            message = 'shadow: telegram',
            twitchChannel = 'smCharles',
            twitchChannelId = charlesUserId
        )

        if ttsMonsterUrls is not None:
            fileUrls.extend(ttsMonsterUrls.urls)

    fileUris = await ttsMonsterFileManager.saveTtsUrlsToNewFiles(fileUrls)

    print(f'{fileUrls=} {fileUris=}')

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
