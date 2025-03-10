import asyncio
from asyncio import AbstractEventLoop

from .google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from .google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from .network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from .network.networkClientProvider import NetworkClientProvider
from .storage.jsonStaticReader import JsonStaticReader
from .storage.tempFileHelper import TempFileHelper
from .storage.tempFileHelperInterface import TempFileHelperInterface
from .streamElements.apiService.streamElementsApiService import StreamElementsApiService
from .streamElements.apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from .streamElements.helper.streamElementsHelper import StreamElementsHelper
from .streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from .streamElements.models.streamElementsVoice import StreamElementsVoice
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
from .twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from .twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class FakeStreamElementsUserKeyRepository(StreamElementsUserKeyRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(self, twitchChannelId: str) -> str | None:
        return ''

    async def remove(self, twitchChannelId: str):
        raise RuntimeError('Not implemented')

    async def set(self, userKey: str | None, twitchChannelId: str):
        raise RuntimeError('Not implemented')

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

tempFileHelper: TempFileHelperInterface = TempFileHelper(
    eventLoop = eventLoop
)

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
    settingsJsonReader = JsonStaticReader(dict())
)

twitchMessageStringUtils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository,
    twitchMessageStringUtils = twitchMessageStringUtils
)

streamElementsApiService: StreamElementsApiServiceInterface = StreamElementsApiService(
    networkClientProvider = networkClientProvider,
    timber = timber
)

streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser(
    streamElementsJsonParser = streamElementsJsonParser
)

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
    tempFileHelper = tempFileHelper,
    timber = timber
)

async def main():
    pass

    message = 'Hello, World!'

    speechBytes = await streamElementsHelper.getSpeech(
        message = message,
        twitchChannel = 'twitchChannel',
        twitchChannelId = 'twitchChannelId',
        voice = StreamElementsVoice.BRIAN
    )

    fileUri: str | None = None

    if speechBytes is not None:
        fileUri = await streamElementsFileManager.saveSpeechToNewFile(speechBytes)

    print(f'{message=} {fileUri=}')

    pass

eventLoop.run_until_complete(main())
