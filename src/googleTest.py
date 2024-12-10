import asyncio
from asyncio import AbstractEventLoop

from .google.apiService.googleApiService import GoogleApiService
from .google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from .google.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from .google.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from .google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from .google.googleJsonMapper import GoogleJsonMapper
from .google.googleJsonMapperInterface import GoogleJsonMapperInterface
from .google.googleJwtBuilder import GoogleJwtBuilder
from .google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from .google.googleTextSynthesisInput import GoogleTextSynthesisInput
from .google.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from .google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from .google.settings.googleSettingsRepository import GoogleSettingsRepository
from .google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .misc.backgroundTaskHelper import BackgroundTaskHelper
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from .network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from .network.networkClientProvider import NetworkClientProvider
from .storage.jsonStaticReader import JsonStaticReader
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .tts.google.googleFileExtensionHelper import GoogleFileExtensionHelper
from .tts.google.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .tts.google.googleTtsFileManager import GoogleTtsFileManager
from .tts.google.googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from .tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from .tts.google.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface


class GoogleCloudProjectCredentialsProvider(GoogleCloudProjectCredentialsProviderInterface):

    async def getGoogleCloudProjectKeyId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectPrivateKey(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
        raise RuntimeError('Not implemented')

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = GoogleCloudProjectCredentialsProvider()

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)
networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber
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

googleTtsFileManager: GoogleTtsFileManagerInterface = GoogleTtsFileManager(
    eventLoop = eventLoop,
    googleFileExtensionHelper = googleFileExtensionHelper,
    googleSettingsRepository = googleSettingsRepository,
    timber = timber
)

googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = GoogleTtsVoiceChooser()

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

    selectionParams = await googleTtsVoiceChooser.choose()

    audioConfig = GoogleVoiceAudioConfig(
        pitch = None,
        speakingRate = None,
        volumeGainDb = None,
        sampleRateHertz = None,
        audioEncoding = await googleSettingsRepository.getVoiceAudioEncoding()
    )

    request = GoogleTextSynthesizeRequest(
        synthesisInput = synthesisInput,
        voice = selectionParams,
        audioConfig = audioConfig
    )

    textToSpeechResult = await googleApiService.textToSpeech(request)
    print(f'text to speech result: {textToSpeechResult=}')

    fileName = await googleTtsFileManager.writeBase64CommandToNewFile(textToSpeechResult.audioContent)
    print(f'{fileName=}')

    pass

eventLoop.run_until_complete(main())
