import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from datetime import datetime
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .microsoftSamApiHelperInterface import MicrosoftSamApiHelperInterface
from .microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ..models.microsoftSamFileReference import MicrosoftSamFileReference
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ..parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ..settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.ttsProvider import TtsProvider


class MicrosoftSamHelper(MicrosoftSamHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        microsoftSamApiHelper: MicrosoftSamApiHelperInterface,
        microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(microsoftSamApiHelper, MicrosoftSamApiHelperInterface):
            raise TypeError(f'microsoftSamApiHelper argument is malformed: \"{microsoftSamApiHelper}\"')
        elif not isinstance(microsoftSamMessageVoiceParser, MicrosoftSamMessageVoiceParserInterface):
            raise TypeError(f'microsoftSamMessageVoiceParser argument is malformed: \"{microsoftSamMessageVoiceParser}\"')
        elif not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__microsoftSamApiHelper: MicrosoftSamApiHelperInterface = microsoftSamApiHelper
        self.__microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface = microsoftSamMessageVoiceParser
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider
        self.__fileExtension: str = fileExtension

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

        self.__timber.log('MicrosoftSamHelper', f'Created new directories ({filePath=})')

    async def __generateFileName(self) -> str:
        fileName = self.__fileNameRegEx.sub('', str(uuid.uuid4())).casefold()
        return f'{fileName}.{self.__fileExtension}'

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MicrosoftSamFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        result = await self.__microsoftSamMessageVoiceParser.determineVoiceFromMessage(message)
        voice: MicrosoftSamVoice

        if result is None:
            voice = await self.__microsoftSamSettingsRepository.getDefaultVoice()
        else:
            voice = result.voice
            message = result.message

        speechBytes = await self.__microsoftSamApiHelper.getSpeech(
            voice = voice,
            message = message
        )

        if speechBytes is None:
            return None

        fileName = await self.__generateFileName()
        filePath = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(TtsProvider.MICROSOFT_SAM)
        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = fileName,
            filePath = filePath
        ):
            return MicrosoftSamFileReference(
                storeDateTime = storeDateTime,
                filePath = f'{filePath}/{fileName}'
            )
        else:
            self.__timber.log('MicrosoftSamHelper', f'Failed to write Microsoft Sam TTS speechBytes to file ({message=}) ({fileName=}) ({filePath=})')
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
            self.__timber.log('MicrosoftSamHelper', f'Encountered exception when trying to write Microsoft Sam TTS speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
