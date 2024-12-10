import traceback

from .googleTtsChoice import GoogleTtsChoice
from .googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from .googleTtsHelperInterface import GoogleTtsHelperInterface
from .googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ...google.googleApiServiceInterface import GoogleApiServiceInterface
from ...google.googleTextSynthesisInput import GoogleTextSynthesisInput
from ...google.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ...google.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ...google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class GoogleTtsHelper(GoogleTtsHelperInterface):

    def __init__(
        self,
        googleApiService: GoogleApiServiceInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsFileManager: GoogleTtsFileManagerInterface,
        googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface,
        timber: TimberInterface
    ):
        if not isinstance(googleApiService, GoogleApiServiceInterface):
            raise TypeError(f'googleApiService argument is malformed: \"{googleApiService}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsFileManager, GoogleTtsFileManagerInterface):
            raise TypeError(f'googleTtsFileManager argument is malformed: \"{googleTtsFileManager}\"')
        elif not isinstance(googleTtsVoiceChooser, GoogleTtsVoiceChooserInterface):
            raise TypeError(f'googleTtsVoiceChooser argument is malformed: \"{googleTtsVoiceChooser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__googleApiService: GoogleApiServiceInterface = googleApiService
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsFileManager: GoogleTtsFileManagerInterface = googleTtsFileManager
        self.__googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = googleTtsVoiceChooser
        self.__timber: TimberInterface = timber

    async def getSpeechFile(self, message: str) -> str | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        ttsChoice = await self.__randomlyChooseTts()

        request = GoogleTextSynthesizeRequest(
            synthesisInput = GoogleTextSynthesisInput(
                text = message
            ),
            voice = ttsChoice.selectionParams,
            audioConfig = ttsChoice.audioConfig
        )

        response: GoogleTextSynthesisResponse | None = None
        exception: Exception | None = None

        try:
            response = await self.__googleApiService.textToSpeech(request)
        except Exception as e:
            exception = e

        if response is None or exception is not None:
            self.__timber.log('GoogleTtsManager', f'Failed to utilize Google Text to Speech API for TTS message ({message=}) ({response=}): {exception}', exception, traceback.format_exc())
            return None

        return await self.__googleTtsFileManager.writeBase64CommandToNewFile(
            base64Command = response.audioContent
        )

    async def __randomlyChooseTts(self) -> GoogleTtsChoice:
        audioConfig = GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = None,
            sampleRateHertz = None,
            audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        )

        selectionParams = await self.__googleTtsVoiceChooser.choose()

        return GoogleTtsChoice(
            audioConfig = audioConfig,
            selectionParams = selectionParams
        )
