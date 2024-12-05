import asyncio
from asyncio import AbstractEventLoop

from .google.googleJsonMapper import GoogleJsonMapper
from .google.googleJsonMapperInterface import GoogleJsonMapperInterface
from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from .network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from .network.networkClientProvider import NetworkClientProvider
from .storage.jsonStaticReader import JsonStaticReader
from .streamElements.apiService.streamElementsApiService import StreamElementsApiService
from .streamElements.apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from .streamElements.helper.streamElementsHelper import StreamElementsHelper
from .streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from .streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from .streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from .streamElements.parser.streamElementsMessageVoiceParser import StreamElementsMessageVoiceParser
from .streamElements.parser.streamElementsMessageVoiceParserInterface import \
    StreamElementsMessageVoiceParserInterface
from .streamElements.settings.streamElementsSettingsRepository import StreamElementsSettingsRepository
from .streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from .streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner
from .streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from .streamElements.userKeyRepository.streamElementsUserKeyRepositoryInterface import \
    StreamElementsUserKeyRepositoryInterface
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .tts.streamElements.streamElementsFileManager import StreamElementsFileManager
from .tts.streamElements.streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from .tts.ttsSettingsRepository import TtsSettingsRepository
from .tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

class FakeStreamElementsUserKeyRepository(StreamElementsUserKeyRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(self, twitchChannelId: str) -> str | None:
        return ''

    async def set(self, userKey: str | None, twitchChannelId: str):
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

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonStaticReader(dict())
)

streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

streamElementsApiService: StreamElementsApiServiceInterface = StreamElementsApiService(
    networkClientProvider = networkClientProvider,
    timber = timber
)

streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser()

streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = StreamElementsSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
    streamElementsJsonParser = streamElementsJsonParser
)

streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface = FakeStreamElementsUserKeyRepository()

streamElementsHelper: StreamElementsHelperInterface = StreamElementsHelper(
    streamElementsApiService = streamElementsApiService,
    streamElementsMessageVoiceParser = streamElementsMessageVoiceParser,
    streamElementsSettingsRepository = streamElementsSettingsRepository,
    streamElementsUserKeyRepository = streamElementsUserKeyRepository,
    timber = timber
)

streamElementsFileManager: StreamElementsFileManagerInterface = StreamElementsFileManager(
    eventLoop = eventLoop,
    timber = timber
)

async def main():
    pass

    message = 'Hello, World!'

    speechBytes = await streamElementsHelper.getSpeech(
        message = message,
        twitchChannel = 'twitchChannel',
        twitchChannelId = 'twitchChannelId'
    )

    fileUri: str | None = None

    if speechBytes is not None:
        fileUri = await streamElementsFileManager.saveSpeechToNewFile(speechBytes)

    print(f'{message=} {fileUri=}')

    pass

eventLoop.run_until_complete(main())