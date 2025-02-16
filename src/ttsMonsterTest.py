import asyncio
from asyncio import AbstractEventLoop

from src.glacialTtsStorage.fileRetriever.glacialTtsFileRetriever import GlacialTtsFileRetriever
from src.glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from src.glacialTtsStorage.idGenerator.glacialTtsIdGenerator import GlacialTtsIdGenerator
from src.glacialTtsStorage.idGenerator.glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from src.glacialTtsStorage.mapper.glacialTtsDataMapper import GlacialTtsDataMapper
from src.glacialTtsStorage.mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from src.glacialTtsStorage.repository.glacialTtsStorageRepository import GlacialTtsStorageRepository
from src.glacialTtsStorage.repository.glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.directoryProvider.ttsDirectoryProvider import TtsDirectoryProvider
from src.tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from src.ttsMonster.apiService.ttsMonsterPrivateApiService import TtsMonsterPrivateApiService
from src.ttsMonster.apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from src.ttsMonster.helper.ttsMonsterHelper import TtsMonsterHelper
from src.ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from src.ttsMonster.helper.ttsMonsterPrivateApiHelper import TtsMonsterPrivateApiHelper
from src.ttsMonster.helper.ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.settings.ttsMonsterSettingsRepository import TtsMonsterSettingsRepository
from src.ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class FakeTtsMonsterKeyAndUserIdRepository(TtsMonsterKeyAndUserIdRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterKeyAndUserId | None:
        raise RuntimeError('Not implemented')


eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

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

ttsDirectoryProvider: TtsDirectoryProviderInterface = TtsDirectoryProvider()

ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface = FakeTtsMonsterKeyAndUserIdRepository()

ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper(
    timber = timber
)

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

ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = TtsMonsterSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

glacialTtsDataMapper: GlacialTtsDataMapperInterface = GlacialTtsDataMapper()

glacialTtsIdGenerator: GlacialTtsIdGeneratorInterface = GlacialTtsIdGenerator()

glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface = GlacialTtsStorageRepository(
    glacialTtsDataMapper = glacialTtsDataMapper,
    glacialTtsIdGenerator = glacialTtsIdGenerator,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = GlacialTtsFileRetriever(
    eventLoop = eventLoop,
    glacialTtsStorageRepository = glacialTtsStorageRepository,
    timber = timber,
    ttsDirectoryProvider = ttsDirectoryProvider
)

ttsMonsterHelper: TtsMonsterHelperInterface = TtsMonsterHelper(
    eventLoop = eventLoop,
    glacialTtsFileRetriever = glacialTtsFileRetriever,
    timber = timber,
    ttsMonsterPrivateApiHelper = ttsMonsterPrivateApiHelper,
    ttsMonsterSettingsRepository = ttsMonsterSettingsRepository
)

twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = TwitchFriendsUserIdRepository()


async def main():
    pass

    twitchChannelId = await twitchFriendsUserIdRepository.getCharlesUserId()

    if not isinstance(twitchChannelId, str):
        raise RuntimeError(f'twitchChannelId value is not set: \"{twitchChannelId}\"')

    message = 'shadow: telegram'
    twitchChannel = 'smCharles'

    fileReference = await ttsMonsterHelper.generateTts(
        message = message,
        twitchChannel = twitchChannel,
        twitchChannelId = twitchChannelId
    )

    print(f'text to speech results: ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({fileReference=})')

    pass

eventLoop.run_until_complete(main())
