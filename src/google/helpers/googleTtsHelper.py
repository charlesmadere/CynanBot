import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from datetime import datetime
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from .googleTtsHelperInterface import GoogleTtsHelperInterface
from .googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ..models.googleTextSynthesisInput import GoogleTextSynthesisInput
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTtsFileReference import GoogleTtsFileReference
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..models.googleVoicePreset import GoogleVoicePreset
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams
from ..settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class GoogleTtsHelper(GoogleTtsHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        googleFileExtensionHelper: GoogleFileExtensionHelperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsApiHelper: GoogleTtsApiHelperInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(googleFileExtensionHelper, GoogleFileExtensionHelperInterface):
            raise TypeError(f'googleFileExtensionHelper argument is malformed: \"{googleFileExtensionHelper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsApiHelper, GoogleTtsApiHelperInterface):
            raise TypeError(f'googleTtsApiHelper argument is malformed: \"{googleTtsApiHelper}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__googleFileExtensionHelper: GoogleFileExtensionHelperInterface = googleFileExtensionHelper
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsApiHelper: GoogleTtsApiHelperInterface = googleTtsApiHelper
        self.__googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface = googleTtsVoicesHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

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

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None
    ) -> str | None:
        if not await self.__googleSettingsRepository.useDonationPrefix():
            return message
        elif utils.isValidStr(donationPrefix) and utils.isValidStr(message):
            return f'{donationPrefix} {message}'
        elif utils.isValidStr(donationPrefix):
            return donationPrefix
        elif utils.isValidStr(message):
            return message
        else:
            return None

    async def __generateFileName(self) -> str:
        fileName = self.__fileNameRegEx.sub('', str(uuid.uuid4())).casefold()
        audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        fileExtension = await self.__googleFileExtensionHelper.getFileExtension(audioEncoding)
        return f'{fileName}.{fileExtension}'

    async def generateTts(
        self,
        voicePreset: GoogleVoicePreset | None,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> GoogleTtsFileReference | None:
        if voicePreset is not None and not isinstance(voicePreset, GoogleVoicePreset):
            raise TypeError(f'voicePreset argument is malformed: \"{voicePreset}\"')
        elif donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message
        )

        if not utils.isValidStr(fullMessage):
            return None

        synthesisInput = GoogleTextSynthesisInput(text = fullMessage)

        if voicePreset is None:
            voicePreset = await self.__googleTtsVoicesHelper.getEnglishVoice()

        voice = GoogleVoiceSelectionParams(
            gender = None,
            languageCode = voicePreset.languageCode,
            name = voicePreset.fullName
        )

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

        fileName = await self.__generateFileName()
        filePath = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(TtsProvider.GOOGLE)
        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = fileName,
            filePath = filePath
        ):
            return GoogleTtsFileReference(
                storeDateTime = storeDateTime,
                filePath = f'{filePath}/{fileName}'
            )
        else:
            self.__timber.log('GoogleTtsHelper', f'Failed to write Google TTS speechBytes to file ({fullMessage=}) ({request=}) ({fileName=}) ({filePath=})')
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
                file = f'{filePath}/{fileName}',
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('GoogleTtsHelper', f'Encountered exception when trying to write Google TTS speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
