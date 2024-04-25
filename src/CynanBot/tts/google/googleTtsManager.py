import random
import traceback
from typing import Any

import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams
from CynanBot.soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.google.googleTtsChoice import GoogleTtsChoice
from CynanBot.tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface
from CynanBot.tts.tempFileHelper.ttsTempFileHelperInterface import \
    TtsTempFileHelperInterface
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
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
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
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__googleApiService: GoogleApiServiceInterface = googleApiService
        self.__googleTtsFileManager: GoogleTtsFileManagerInterface = googleTtsFileManager
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

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

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('GoogleTtsManager', f'Failed to write TTS message in \"{event.getTwitchChannel()}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoading = False
            return False

        self.__timber.log('GoogleTtsManager', f'Playing TTS message in \"{event.getTwitchChannel()}\" from \"{fileName}\"...')
        await self.__soundPlayerManager.playSoundFile(fileName)
        await self.__ttsTempFileHelper.registerTempFile(fileName)
        self.__isLoading = False

        return True

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        message = await self.__ttsCommandBuilder.buildAndCleanEvent(event)

        if not utils.isValidStr(message):
            return None

        ttsChoice = await self.__randomlyChooseTts()

        request = GoogleTextSynthesizeRequest(
            input = GoogleTextSynthesisInput(
                text = message
            ),
            voice = ttsChoice.getSelectionParams(),
            audioConfig = ttsChoice.getAudioConfig()
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

    async def __randomlyChooseTts(self) -> GoogleTtsChoice:
        audioConfig = GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = await self.__ttsSettingsRepository.getGoogleVolumeGainDb(),
            sampleRateHertz = None,
            audioEncoding = await self.__ttsSettingsRepository.getGoogleVoiceAudioEncoding()
        )

        languageCodes: list[str] = [ 'en-AU', 'en-GB', 'en-US', 'fr-CA', 'ja-JP', 'sv-SE' ]
        languageCode = random.choice(languageCodes)

        names: list[str] | None = None

        if languageCode == 'en-AU':
            names = [ 'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D', 'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D' ]
        elif languageCode == 'en-GB':
            names = [ 'en-GB-Neural2-A', 'en-GB-Neural2-B', 'en-GB-Neural2-C', 'en-GB-Neural2-D', 'en-GB-Neural2-F', 'en-GB-Wavenet-A', 'en-GB-Wavenet-B', 'en-GB-Wavenet-C', 'en-GB-Wavenet-D', 'en-GB-Wavenet-F' ]
        elif languageCode == 'en-US':
            names = [ 'en-US-Casual-K', 'en-US-Journey-D', 'en-US-Journey-F' ]
        elif languageCode == 'fr-CA':
            names = [ 'fr-CA-Wavenet-A', 'fr-CA-Wavenet-B', 'fr-CA-Wavenet-C', 'fr-CA-Wavenet-D' ]
        elif languageCode == 'ja-JP':
            names = [ 'ja-JP-Neural2-B', 'ja-JP-Neural2-C', 'ja-JP-Neural2-D' ]
        elif languageCode == 'sv-SE':
            names = [ 'sv-SE-Wavenet-A', 'sv-SE-Wavenet-B', 'sv-SE-Wavenet-C', 'sv-SE-Wavenet-D', 'sv-SE-Wavenet-E' ]

        name: str | None = None

        if names is not None and len(names) >= 1:
            name = random.choice(names)

        selectionParams = GoogleVoiceSelectionParams(
            gender = None,
            languageCode = languageCode,
            name = name
        )

        return GoogleTtsChoice(
            audioConfig = audioConfig,
            selectionParams = selectionParams
        )

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isLoading': self.__isLoading
        }
