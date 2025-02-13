import asyncio
from asyncio import AbstractEventLoop

from .google.accessToken.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from .google.accessToken.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from .google.apiService.googleApiService import GoogleApiService
from .google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from .google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from .google.helpers.googleFileExtensionHelper import GoogleFileExtensionHelper
from .google.helpers.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from .google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from .google.jwtBuilder.googleJwtBuilder import GoogleJwtBuilder
from .google.jwtBuilder.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from .google.models.googleTextSynthesisInput import GoogleTextSynthesisInput
from .google.models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from .google.models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
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
from .storage.tempFileHelper import TempFileHelper
from .storage.tempFileHelperInterface import TempFileHelperInterface
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .tts.google.googleTtsFileManager import GoogleTtsFileManager
from .tts.google.googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from .tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from .tts.google.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface


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

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

tempFileHelper: TempFileHelperInterface = TempFileHelper(
    eventLoop = eventLoop
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
    tempFileHelper = tempFileHelper,
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
