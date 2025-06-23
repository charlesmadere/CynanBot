import re
import traceback
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from .googleTtsHelperInterface import GoogleTtsHelperInterface
from .googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ..exceptions import GoogleFailedToCreateDirectoriesException
from ..jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from ..models.googleTextSynthesisInput import GoogleTextSynthesisInput
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTtsFileReference import GoogleTtsFileReference
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..models.googleVoicePreset import GoogleVoicePreset
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams
from ..settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class GoogleTtsHelper(GoogleTtsHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        googleFileExtensionHelper: GoogleFileExtensionHelperInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsApiHelper: GoogleTtsApiHelperInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(googleFileExtensionHelper, GoogleFileExtensionHelperInterface):
            raise TypeError(f'googleFileExtensionHelper argument is malformed: \"{googleFileExtensionHelper}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsApiHelper, GoogleTtsApiHelperInterface):
            raise TypeError(f'googleTtsApiHelper argument is malformed: \"{googleTtsApiHelper}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__googleFileExtensionHelper: GoogleFileExtensionHelperInterface = googleFileExtensionHelper
        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsApiHelper: GoogleTtsApiHelperInterface = googleTtsApiHelper
        self.__googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface = googleTtsVoicesHelper
        self.__timber: TimberInterface = timber

        self.__directoryTreeRegEx: Pattern = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise GoogleFailedToCreateDirectoriesException(f'Failed to create Google TTS file directories ({filePath=}) ({directoryMatch=})')

        directory = directoryMatch.group(1)

        if await aiofiles.ospath.exists(
            path = directory,
            loop = self.__eventLoop
        ):
            return

        await aiofiles.os.makedirs(
            name = directory,
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

        if voicePreset is None:
            voicePreset = await self.__googleTtsVoicesHelper.getEnglishVoice()

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = fullMessage,
            voice = voicePreset.fullName,
            provider = TtsProvider.GOOGLE
        )

        if glacialFile is not None:
            return GoogleTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voicePreset = await self.__googleJsonMapper.requireVoicePreset(glacialFile.voice)
            )

        synthesisInput = GoogleTextSynthesisInput(
            text = fullMessage
        )

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
            audioConfig = audioConfig,
            voice = voice
        )

        speechBytes = await self.__googleTtsApiHelper.getSpeech(
            request = request
        )

        if speechBytes is None:
            return None

        audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        fileExtension = await self.__googleFileExtensionHelper.getFileExtension(audioEncoding)

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = fileExtension,
            message = fullMessage,
            voice = await self.__googleJsonMapper.serializeVoicePreset(voicePreset),
            provider = TtsProvider.GOOGLE
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath
        ):
            return GoogleTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                voicePreset = voicePreset,
                filePath = glacialFile.filePath
            )
        else:
            self.__timber.log('GoogleTtsHelper', f'Failed to write Google TTS speechBytes to file ({fullMessage=}) ({request=})')
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
            self.__timber.log('GoogleTtsHelper', f'Encountered exception when trying to write Google TTS speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
