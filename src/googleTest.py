import asyncio
from asyncio import AbstractEventLoop

from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.google.googleApiAccessTokenStorage import \
    GoogleApiAccessTokenStorage
from CynanBot.google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from CynanBot.google.googleApiService import GoogleApiService
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleCloudProjectCredentialsProviderInterface import \
    GoogleCloudProjectCredentialsProviderInterface
from CynanBot.google.googleJsonMapper import GoogleJsonMapper
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleJwtBuilder import GoogleJwtBuilder
from CynanBot.google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.tts.google.googleFileExtensionHelper import \
    GoogleFileExtensionHelper
from CynanBot.tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface
from CynanBot.tts.google.googleTtsFileManager import GoogleTtsFileManager
from CynanBot.tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface
from CynanBot.tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from CynanBot.tts.google.googleTtsVoiceChooserInterface import \
    GoogleTtsVoiceChooserInterface
from CynanBot.tts.ttsSettingsRepository import TtsSettingsRepository
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


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

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber
)

googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = GoogleCloudProjectCredentialsProvider()

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    timber = timber
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = googleCloudProjectCredentialsProvider,
    googleJsonMapper = googleJsonMapper
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

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonStaticReader(dict())
)

googleTtsFileManager: GoogleTtsFileManagerInterface = GoogleTtsFileManager(
    eventLoop = eventLoop,
    googleFileExtensionHelper = googleFileExtensionHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository
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

    input = GoogleTextSynthesisInput(
        text = 'sheeples timed out aniv for 60 seconds! ripbozo'
    )

    selectionParams = await googleTtsVoiceChooser.choose()

    audioConfig = GoogleVoiceAudioConfig(
        pitch = None,
        speakingRate = None,
        volumeGainDb = await ttsSettingsRepository.getGoogleVolumeGainDb(),
        sampleRateHertz = None,
        audioEncoding = await ttsSettingsRepository.getGoogleVoiceAudioEncoding()
    )

    request = GoogleTextSynthesizeRequest(
        input = input,
        voice = selectionParams,
        audioConfig = audioConfig
    )

    textToSpeechResult = await googleApiService.textToSpeech(request)
    print(f'text to speech result: {textToSpeechResult=}')

    fileName = await googleTtsFileManager.writeBase64CommandToNewFile(textToSpeechResult.getAudioContent())
    print(f'{fileName=}')

    pass

eventLoop.run_until_complete(main())
