import traceback
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from .googleTtsHelperInterface import GoogleTtsHelperInterface
from ..models.googleTextSynthesisInput import GoogleTextSynthesisInput
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTtsFileReference import GoogleTtsFileReference
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ..voiceChooser.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface


class GoogleTtsHelper(GoogleTtsHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsApiHelper: GoogleTtsApiHelperInterface,
        googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsApiHelper, GoogleTtsApiHelperInterface):
            raise TypeError(f'googleTtsApiHelper argument is malformed: \"{googleTtsApiHelper}\"')
        elif not isinstance(googleTtsVoiceChooser, GoogleTtsVoiceChooserInterface):
            raise TypeError(f'googleTtsVoiceChooser argument is malformed: \"{googleTtsVoiceChooser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsApiHelper: GoogleTtsApiHelperInterface = googleTtsApiHelper
        self.__googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = googleTtsVoiceChooser
        self.__timber: TimberInterface = timber
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider

    async def __createDirectories(self, filePath: str):
        if await aiofiles.ospath.exists(
            path = filePath,
            loop = self.__eventLoop
        ):
            return

        await aiofiles.os.makedirs(
            name = filePath,
            loop = self.__eventLoop
        )

        self.__timber.log('GoogleTtsHelper', f'Created new directories ({filePath=})')

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> GoogleTtsFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        synthesisInput = GoogleTextSynthesisInput(
            text = message
        )

        voice = await self.__googleTtsVoiceChooser.choose()

        audioConfig = GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = await self.__googleSettingsRepository.getVolumeGainDb(),
            sampleRateHertz = None,
            audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        )

        request = GoogleTextSynthesizeRequest(
            synthesisInput = synthesisInput,
            voice = voice,
            audioConfig = audioConfig
        )

        speechBytes = await self.__googleTtsApiHelper.getSpeech(
            request = request
        )

        if speechBytes is None:
            return None

        # TODO get actual directory and file names
        fileName = 'fileName.mp3'
        filePath = 'google'

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = fileName,
            filePath = filePath
        ):
            return GoogleTtsFileReference(filePath = filePath)
        else:
            self.__timber.log('GoogleTtsHelper', f'Failed to write Google TTS speechBytes to file ({message=}) ({filePath=})')
            return None

    async def __saveSpeechBytes(
        self,
        speechBytes: bytes,
        fileName: str,
        filePath: str
    ) -> bool:
        if not isinstance(speechBytes, bytes):
            raise TypeError(f'speechBytes argument is malformed: \"{speechBytes}\"')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        await self.__createDirectories(filePath)

        try:
            async with aiofiles.open(
                file = filePath,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('GoogleTtsHelper', f'Encountered exception when trying to write Google TTS speechBytes to file ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
