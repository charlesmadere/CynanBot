import traceback

import CynanBot.misc.utils as utils
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams
from CynanBot.soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface
from CynanBot.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class GoogleTtsManager(TtsManagerInterface):

    def __init__(
        self,
        googleApiService: GoogleApiServiceInterface,
        googleTtsFileManager: GoogleTtsFileManagerInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(googleApiService, GoogleApiServiceInterface):
            raise TypeError(f'googleApiService argument is malformed: \"{googleApiService}"')
        elif not isinstance(googleTtsFileManager, GoogleTtsFileManagerInterface):
            raise TypeError(f'googleTtsFileManager argument is malformed: \"{googleTtsFileManager}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__googleApiService: GoogleApiServiceInterface = googleApiService
        self.__googleTtsFileManager: GoogleTtsFileManagerInterface = googleTtsFileManager
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoading: bool = False

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to Google TTS,
        #  and yet in this scenario, this method would still return true. So for the fix for this
        #  is probably a way to check if SoundPlayerManager is currently playing, AND also a check
        #  to see specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('GoogleTtsManager', f'There is already an ongoing Google TTS event!')
            return False

        self.__isLoading = True
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName):
            self.__isLoading = False
            return False

        self.__timber.log('GoogleTtsManager', f'Playing TTS message in \"{event.getTwitchChannel()}\" from \"{fileName}\"...')
        await self.__soundPlayerManager.playSoundFile(fileName)
        await self.__googleTtsFileManager.deleteFile(fileName)
        self.__isLoading = False

        return True

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        message = await self.__ttsCommandBuilder.buildAndCleanEvent(event)

        if not utils.isValidStr(message):
            return None

        request = GoogleTextSynthesizeRequest(
            input = GoogleTextSynthesisInput(
                text = message
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
        )

        response: GoogleTextSynthesisResponse | None = None
        exception: Exception | None = None

        try:
            response = await self.__googleApiService.textToSpeech(request)
        except Exception as e:
            exception = e

        if response is None:
            self.__timber.log('GoogleTtsManager', f'Failed to utilize Google Text to Speech API for TTS event ({event=}) ({response=}): {exception}', exception, traceback.format_exc())
            return None

        return await self.__googleTtsFileManager.writeBase64CommandToNewFile(
            base64Command = response.getAudioContent()
        )

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, object]:
        return {
            'isLoading': self.__isLoading
        }
