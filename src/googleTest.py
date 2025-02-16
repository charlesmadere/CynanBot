import asyncio
from asyncio import AbstractEventLoop

from src.google.accessToken.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from src.google.accessToken.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from src.google.apiService.googleApiService import GoogleApiService
from src.google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from src.google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from src.google.helpers.googleFileExtensionHelper import GoogleFileExtensionHelper
from src.google.helpers.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.jwtBuilder.googleJwtBuilder import GoogleJwtBuilder
from src.google.jwtBuilder.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from src.google.models.googleTextSynthesisInput import GoogleTextSynthesisInput
from src.google.settings.googleSettingsRepository import GoogleSettingsRepository
from src.google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
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


class FakeGoogleCloudProjectCredentialsProvider(GoogleCloudProjectCredentialsProviderInterface):

    async def getGoogleCloudProjectKeyId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectPrivateKey(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
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

googleFileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

googleSettingsRepository: GoogleSettingsRepositoryInterface = GoogleSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonStaticReader(dict())
)

async def main():
    pass

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

    synthesisInput = GoogleTextSynthesisInput(
        text = 'sheeples23 timed out aniv for 60 seconds! rip bozo!'
    )

    # selectionParams = await googleTtsVoiceChooser.choose()
    #
    # audioConfig = GoogleVoiceAudioConfig(
    #     pitch = None,
    #     speakingRate = None,
    #     volumeGainDb = None,
    #     sampleRateHertz = None,
    #     audioEncoding = await googleSettingsRepository.getVoiceAudioEncoding()
    # )
    #
    # request = GoogleTextSynthesizeRequest(
    #     synthesisInput = synthesisInput,
    #     voice = selectionParams,
    #     audioConfig = audioConfig
    # )
    #
    # textToSpeechResult = await googleApiService.textToSpeech(request)
    # print(f'text to speech result: {textToSpeechResult=}')

    pass

eventLoop.run_until_complete(main())
