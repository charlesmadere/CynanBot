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
from src.ttsMonster.helpers.ttsMonsterHelper import TtsMonsterHelper
from src.ttsMonster.helpers.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from src.ttsMonster.helpers.ttsMonsterPrivateApiHelper import TtsMonsterPrivateApiHelper
from src.ttsMonster.helpers.ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.messageChunkParser.ttsMonsterMessageChunkParser import TtsMonsterMessageChunkParser
from src.ttsMonster.messageChunkParser.ttsMonsterMessageChunkParserInterface import \
    TtsMonsterMessageChunkParserInterface
from src.ttsMonster.models.ttsMonsterTokens import TtsMonsterTokens
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from src.ttsMonster.settings.ttsMonsterSettingsRepository import TtsMonsterSettingsRepository
from src.ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from src.ttsMonster.tokens.ttsMonsterTokensRepositoryInterface import \
    TtsMonsterTokensRepositoryInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class FakeTtsMonsterTokensRepository(TtsMonsterTokensRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(
        self,
        twitchChannelId: str,
    ) -> TtsMonsterTokens | None:
        raise RuntimeError('Not implemented')

    async def set(
        self,
        ttsMonsterKey: str | None,
        ttsMonsterUserId: str | None,
        twitchChannelId: str,
    ):
        raise RuntimeError(f'Not implemented')


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

ttsMonsterTokensRepository: TtsMonsterTokensRepositoryInterface = FakeTtsMonsterTokensRepository()

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
    ttsMonsterTokensRepository = ttsMonsterTokensRepository,
    ttsMonsterPrivateApiService = ttsMonsterPrivateApiService
)

ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = TtsMonsterSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
    ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
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

ttsMonsterMessageChunkParser: TtsMonsterMessageChunkParserInterface = TtsMonsterMessageChunkParser()

ttsMonsterHelper: TtsMonsterHelperInterface = TtsMonsterHelper(
    eventLoop = eventLoop,
    glacialTtsFileRetriever = glacialTtsFileRetriever,
    timber = timber,
    ttsMonsterMessageChunkParser = ttsMonsterMessageChunkParser,
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
        donationPrefix = None,
        message = message,
        twitchChannel = twitchChannel,
        twitchChannelId = twitchChannelId,
        voice = TtsMonsterVoice.SHADOW
    )

    print(f'text to speech results: ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({fileReference=})')

    pass

eventLoop.run_until_complete(main())
