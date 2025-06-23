import re
import traceback
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .microsoftTtsApiHelperInterface import MicrosoftTtsApiHelperInterface
from .microsoftTtsHelperInterface import MicrosoftTtsHelperInterface
from ..exceptions import MicrosoftTtsFailedToCreateDirectoriesException
from ..models.microsoftTtsFileReference import MicrosoftTtsFileReference
from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ..parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from ..parser.microsoftTtsMessageVoiceParserInterface import MicrosoftTtsMessageVoiceParserInterface
from ..settings.microsoftTtsSettingsRepositoryInterface import MicrosoftTtsSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class MicrosoftTtsHelper(MicrosoftTtsHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        microsoftTtsApiHelper: MicrosoftTtsApiHelperInterface,
        microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface,
        microsoftTtsMessageVoiceParser: MicrosoftTtsMessageVoiceParserInterface,
        microsoftTtsSettingsRepository: MicrosoftTtsSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(microsoftTtsApiHelper, MicrosoftTtsApiHelperInterface):
            raise TypeError(f'microsoftTtsApiHelper argument is malformed: \"{microsoftTtsApiHelper}\"')
        elif not isinstance(microsoftTtsJsonParser, MicrosoftTtsJsonParserInterface):
            raise TypeError(f'microsoftTtsJsonParser argument is malformed: \"{microsoftTtsJsonParser}\"')
        elif not isinstance(microsoftTtsMessageVoiceParser, MicrosoftTtsMessageVoiceParserInterface):
            raise TypeError(f'microsoftTtsMessageVoiceParser argument is malformed: \"{microsoftTtsMessageVoiceParser}\"')
        elif not isinstance(microsoftTtsSettingsRepository, MicrosoftTtsSettingsRepositoryInterface):
            raise TypeError(f'microsoftTtsSettingsRepository argument is malformed: \"{microsoftTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__microsoftTtsApiHelper: MicrosoftTtsApiHelperInterface = microsoftTtsApiHelper
        self.__microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface = microsoftTtsJsonParser
        self.__microsoftTtsMessageVoiceParser: MicrosoftTtsMessageVoiceParserInterface = microsoftTtsMessageVoiceParser
        self.__microsoftTtsSettingsRepository: MicrosoftTtsSettingsRepositoryInterface = microsoftTtsSettingsRepository
        self.__timber: TimberInterface = timber

        self.__directoryTreeRegEx: Pattern = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise MicrosoftTtsFailedToCreateDirectoriesException(f'Failed to create Microsoft file directories ({filePath=}) ({directoryMatch=})')

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

        self.__timber.log('MicrosoftTtsHelper', f'Created new directories ({filePath=}) ({directory=})')

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None
    ) -> str | None:
        if not await self.__microsoftTtsSettingsRepository.useDonationPrefix():
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
        voice: MicrosoftTtsVoice | None,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MicrosoftTtsFileReference | None:
        if voice is not None and not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
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

        if voice is None:
            voice = await self.__microsoftTtsSettingsRepository.getDefaultVoice()

        messageVoiceResult = await self.__microsoftTtsMessageVoiceParser.determineVoiceFromMessage(message)

        if messageVoiceResult is not None:
            message = messageVoiceResult.message
            voice = messageVoiceResult.voice

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message
        )

        if not utils.isValidStr(fullMessage):
            return None

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = fullMessage,
            voice = await self.__microsoftTtsJsonParser.serializeVoice(voice),
            provider = TtsProvider.MICROSOFT
        )

        if glacialFile is not None:
            return MicrosoftTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = await self.__microsoftTtsJsonParser.requireVoice(glacialFile.voice)
            )

        speechBytes = await self.__microsoftTtsApiHelper.getSpeech(
            voice = voice,
            message = fullMessage
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = await self.__microsoftTtsSettingsRepository.getFileExtension(),
            message = fullMessage,
            voice = await self.__microsoftTtsJsonParser.serializeVoice(voice),
            provider = TtsProvider.MICROSOFT
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath
        ):
            return MicrosoftTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = voice
            )
        else:
            self.__timber.log('MicrosoftTtsHelper', f'Failed to write Microsoft TTS speechBytes to file ({fullMessage=}) ({glacialFile=})')
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
            self.__timber.log('MicrosoftTtsHelper', f'Encountered exception when trying to write Microsoft speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
