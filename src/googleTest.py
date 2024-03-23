import asyncio
from asyncio import AbstractEventLoop

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
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.google.googleVoiceGender import GoogleVoiceGender
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class GoogleCloudProjectCredentialsProvider(GoogleCloudProjectCredentialsProviderInterface):

    async def getGoogleCloudApiKey(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectKeyId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudProjectId(self) -> str | None:
        raise RuntimeError('Not implemented')

    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
        raise RuntimeError('Not implemented')

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

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

async def main():
    pass

    translationResult = await googleApiService.translate(GoogleTranslationRequest(
        glossaryConfig = None,
        transliterationConfig = None,
        contents = [ 'Hello, World!' ],
        mimeType = 'text/plain',
        model = None,
        sourceLanguageCode = 'ja',
        targetLanguageCode = 'en-us'
    ))

    print(f'translation result: {translationResult}')

    textToSpeechResult = await googleApiService.textToSpeech(GoogleTextSynthesizeRequest(
        input = GoogleTextSynthesisInput(
            text = 'Hello, World!'
        ),
        voice = GoogleVoiceSelectionParams(
            gender = None,
            languageCode = 'en-us',
            name = None
        ),
        audioConfig = GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = None,
            sampleRateHertz = None,
            audioEncoding = GoogleVoiceAudioEncoding.MP3
        )
    ))

    print(f'text to speech result: {textToSpeechResult}')

    pass

eventLoop.run_until_complete(main())
