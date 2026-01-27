import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.glacialTtsStorage.fileRetriever.glacialTtsFileRetriever import GlacialTtsFileRetriever
from src.glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from src.glacialTtsStorage.idGenerator.glacialTtsIdGenerator import GlacialTtsIdGenerator
from src.glacialTtsStorage.idGenerator.glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from src.glacialTtsStorage.mapper.glacialTtsDataMapper import GlacialTtsDataMapper
from src.glacialTtsStorage.mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from src.glacialTtsStorage.repository.glacialTtsStorageRepository import GlacialTtsStorageRepository
from src.glacialTtsStorage.repository.glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from src.glacialTtsStorage.stub.stubGlacialTtsFileRetriever import StubGlacialTtsFileRetriever
from src.google.accessToken.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from src.google.accessToken.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from src.google.apiService.googleApiService import GoogleApiService
from src.google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from src.google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from src.google.helpers.googleFileExtensionHelper import GoogleFileExtensionHelper
from src.google.helpers.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from src.google.helpers.googleTtsApiHelper import GoogleTtsApiHelper
from src.google.helpers.googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from src.google.helpers.googleTtsHelper import GoogleTtsHelper
from src.google.helpers.googleTtsHelperInterface import GoogleTtsHelperInterface
from src.google.helpers.googleTtsVoicesHelper import GoogleTtsVoicesHelper
from src.google.helpers.googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.jwtBuilder.googleJwtBuilder import GoogleJwtBuilder
from src.google.jwtBuilder.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from src.google.settings.googleSettingsRepository import GoogleSettingsRepository
from src.google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from src.language.languageEntry import LanguageEntry
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.soundPlayerManager.audioPlayer.audioPlayerSoundPlayerManager import AudioPlayerSoundPlayerManager
from src.soundPlayerManager.settings.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.settings.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.directoryProvider.ttsDirectoryProvider import TtsDirectoryProvider
from src.tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class FakeGoogleCloudProjectCredentialsProvider(GoogleCloudProjectCredentialsProviderInterface):

    async def getGoogleCloudProjectKeyId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectPrivateKey(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
        raise RuntimeError('Not implemented')


eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

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

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = FakeGoogleCloudProjectCredentialsProvider()

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = googleCloudProjectCredentialsProvider,
    googleJsonMapper = googleJsonMapper,
    timeZoneRepository = timeZoneRepository
)

googleApiService: GoogleApiServiceInterface = GoogleApiService(
    googleApiAccessTokenStorage = googleApiAccessTokenStorage,
    googleCloudProjectCredentialsProvider = googleCloudProjectCredentialsProvider,
    googleJsonMapper = googleJsonMapper,
    googleJwtBuilder = googleJwtBuilder,
    networkClientProvider = networkClientProvider,
    timber = timber
)

googleSettingsRepository: GoogleSettingsRepositoryInterface = GoogleSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonStaticReader(dict())
)

googleTtsApiHelper: GoogleTtsApiHelperInterface = GoogleTtsApiHelper(
    googleApiService = googleApiService,
    timber = timber
)

glacialTtsDataMapper: GlacialTtsDataMapperInterface = GlacialTtsDataMapper()

glacialTtsIdGenerator: GlacialTtsIdGeneratorInterface = GlacialTtsIdGenerator()

glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface = GlacialTtsStorageRepository(
    glacialTtsDataMapper = glacialTtsDataMapper,
    glacialTtsIdGenerator = glacialTtsIdGenerator,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

ttsDirectoryProvider: TtsDirectoryProviderInterface = TtsDirectoryProvider()

glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = GlacialTtsFileRetriever(
    eventLoop = eventLoop,
    glacialTtsStorageRepository = glacialTtsStorageRepository,
    timber = timber,
    ttsDirectoryProvider = ttsDirectoryProvider
)

stubGlacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = StubGlacialTtsFileRetriever(
    timeZoneRepository = timeZoneRepository,
    ttsDirectoryProvider = ttsDirectoryProvider
)

googleFileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = GoogleTtsVoicesHelper(
    googleSettingsRepository = googleSettingsRepository,
)

googleTtsHelper: Final[GoogleTtsHelperInterface] = GoogleTtsHelper(
    eventLoop = eventLoop,
    glacialTtsFileRetriever = stubGlacialTtsFileRetriever,
    googleFileExtensionHelper = googleFileExtensionHelper,
    googleJsonMapper = googleJsonMapper,
    googleSettingsRepository = googleSettingsRepository,
    googleTtsApiHelper = googleTtsApiHelper,
    googleTtsVoicesHelper = googleTtsVoicesHelper,
    timber = timber,
)

twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = TwitchFriendsUserIdRepository()

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

soundPlayerManager: SoundPlayerManagerInterface = AudioPlayerSoundPlayerManager(
    eventLoop = eventLoop,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)


async def main():
    pass

    twitchChannelId = await twitchFriendsUserIdRepository.getCharlesUserId()

    if not isinstance(twitchChannelId, str):
        raise RuntimeError(f'twitchChannelId value is not set: \"{twitchChannelId}\"')

    # translationResult = await googleApiService.translate(GoogleTranslationRequest(
    #     glossaryConfig = None,
    #     transliterationConfig = None,
    #     contents = [ 'Hello, World!' ],
    #     mimeType = 'text/plain',
    #     model = None,
    #     sourceLanguageCode = 'en-us',
    #     targetLanguageCode = 'ja'
    # ))

    # print(f'translation result: {translationResult}')

    message = f'Welcome in everyone from Eddie\'s stream! Thanks for the raid. ありがとうございます！'

    fileReference = await googleTtsHelper.generateTts(
        voicePreset = await googleTtsVoicesHelper.getVoiceForLanguage(LanguageEntry.SWEDISH),
        allowMultiSpeaker = True,
        donationPrefix = None,
        message = message,
        twitchChannelId = twitchChannelId,
    )

    if fileReference is None:
        raise RuntimeError(f'expected a non None fileReference: \"{fileReference}\"')

    print(f'text to speech results: ({message=}) ({twitchChannelId=}) ({fileReference=})')

    await soundPlayerManager.playSoundFile(
        filePath = fileReference.filePath,
        volume = await googleSettingsRepository.getMediaPlayerVolume(),
    )

    pass

eventLoop.run_until_complete(main())
