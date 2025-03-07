import re
import traceback
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .microsoftSamApiHelperInterface import MicrosoftSamApiHelperInterface
from .microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ..exceptions import MicrosoftSamFailedToCreateDirectoriesException
from ..models.microsoftSamFileReference import MicrosoftSamFileReference
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ..parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ..parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ..settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class MicrosoftSamHelper(MicrosoftSamHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        microsoftSamApiHelper: MicrosoftSamApiHelperInterface,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(microsoftSamApiHelper, MicrosoftSamApiHelperInterface):
            raise TypeError(f'microsoftSamApiHelper argument is malformed: \"{microsoftSamApiHelper}\"')
        elif not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
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

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__microsoftSamApiHelper: MicrosoftSamApiHelperInterface = microsoftSamApiHelper
        self.__microsoftSamJsonParser: MicrosoftSamJsonParserInterface = microsoftSamJsonParser
        self.__microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface = microsoftSamMessageVoiceParser
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider

        self.__directoryTreeRegEx: Pattern = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise MicrosoftSamFailedToCreateDirectoriesException(f'Failed to create Microsoft Sam file directories ({filePath=}) ({directoryMatch=})')

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

        self.__timber.log('MicrosoftSamHelper', f'Created new directories ({directory=})')

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

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = message,
            voice = await self.__microsoftSamJsonParser.serializeVoice(voice),
            provider = TtsProvider.MICROSOFT_SAM
        )

        if glacialFile is not None:
            return MicrosoftSamFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = await self.__microsoftSamJsonParser.requireVoice(glacialFile.voice)
            )

        speechBytes = await self.__microsoftSamApiHelper.getSpeech(
            voice = voice,
            message = message
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = await self.__microsoftSamSettingsRepository.getFileExtension(),
            message = message,
            voice = await self.__microsoftSamJsonParser.serializeVoice(voice),
            provider = TtsProvider.MICROSOFT_SAM
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath
        ):
            return MicrosoftSamFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = voice
            )
        else:
            self.__timber.log('MicrosoftSamHelper', f'Failed to write Microsoft Sam TTS speechBytes to file ({message=}) ({glacialFile=})')
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
