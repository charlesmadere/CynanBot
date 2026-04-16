import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from src.glacialTtsStorage.stub.stubGlacialTtsFileRetriever import StubGlacialTtsFileRetriever
from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.soundPlayerManager.audioPlayer.audioPlayerSoundPlayerManager import AudioPlayerSoundPlayerManager
from src.soundPlayerManager.settings.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.settings.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.streamElements.apiService.streamElementsApiService import StreamElementsApiService
from src.streamElements.apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from src.streamElements.helper.streamElementsApiHelper import StreamElementsApiHelper
from src.streamElements.helper.streamElementsApiHelperInterface import StreamElementsApiHelperInterface
from src.streamElements.helper.streamElementsHelper import StreamElementsHelper
from src.streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.streamElements.parser.streamElementsMessageVoiceParser import StreamElementsMessageVoiceParser
from src.streamElements.parser.streamElementsMessageVoiceParserInterface import \
    StreamElementsMessageVoiceParserInterface
from src.streamElements.settings.streamElementsSettingsRepository import StreamElementsSettingsRepository
from src.streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from src.streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner
from src.streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from src.streamElements.userKeyRepository.streamElementsUserKeyRepositoryInterface import \
    StreamElementsUserKeyRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.directoryProvider.ttsDirectoryProvider import TtsDirectoryProvider
from src.tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.settings.ttsSettingsRepository import TtsSettingsRepository
from src.tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class FakeStreamElementsUserKeyRepository(StreamElementsUserKeyRepositoryInterface):

    async def clearCaches(self):
        pass

    async def get(self, twitchChannelId: str) -> str | None:
        return ''

    async def remove(self, twitchChannelId: str):
        raise RuntimeError('Not implemented')

    async def set(self, userKey: str | None, twitchChannelId: str):
        raise RuntimeError('Not implemented')

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: Final[TimberInterface] = TimberStub()

timeZoneRepository: Final[TimeZoneRepositoryInterface] = TimeZoneRepository()

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop,
)

networkClientProvider: Final[NetworkClientProvider] = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber,
)

googleJsonMapper: Final[GoogleJsonMapperInterface] = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

ttsJsonMapper: Final[TtsJsonMapperInterface] = TtsJsonMapper(
    timber = timber,
)

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
    ttsJsonMapper = ttsJsonMapper,
)

streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository,
)

streamElementsApiService: StreamElementsApiServiceInterface = StreamElementsApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
)

streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser(
    streamElementsJsonParser = streamElementsJsonParser,
)

streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = StreamElementsSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
    streamElementsJsonParser = streamElementsJsonParser,
)

streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface = FakeStreamElementsUserKeyRepository()

streamElementsApiHelper: StreamElementsApiHelperInterface = StreamElementsApiHelper(
    streamElementsApiService = streamElementsApiService,
    streamElementsUserKeyRepository = streamElementsUserKeyRepository,
    timber = timber,
)

ttsDirectoryProvider: TtsDirectoryProviderInterface = TtsDirectoryProvider()

glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = StubGlacialTtsFileRetriever(
    timeZoneRepository = timeZoneRepository,
    ttsDirectoryProvider = ttsDirectoryProvider,
)

streamElementsHelper: StreamElementsHelperInterface = StreamElementsHelper(
    eventLoop = eventLoop,
    glacialTtsFileRetriever = glacialTtsFileRetriever,
    streamElementsApiHelper = streamElementsApiHelper,
    streamElementsJsonParser = streamElementsJsonParser,
    streamElementsMessageVoiceParser = streamElementsMessageVoiceParser,
    streamElementsSettingsRepository = streamElementsSettingsRepository,
    timber = timber,
)

soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
)

soundPlayerManager: Final[SoundPlayerManagerInterface] = AudioPlayerSoundPlayerManager(
    eventLoop = eventLoop,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

async def main():
    pass

    message = 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'

    fileReference = await streamElementsHelper.generateTts(
        donationPrefix = None,
        message = message,
        twitchChannelId = 'twitchChannelId',
        voice = StreamElementsVoice.BRIAN,
    )

    print(f'text to speech results: ({message=}) ({fileReference=})')

    if fileReference is not None:
        await soundPlayerManager.playSoundFile(
            filePath = fileReference.filePath,
            volume = await streamElementsSettingsRepository.getMediaPlayerVolume(),
        )

    pass

eventLoop.run_until_complete(main())
