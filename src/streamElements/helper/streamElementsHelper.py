import re
import traceback
from asyncio import AbstractEventLoop
from typing import Final, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .streamElementsApiHelperInterface import StreamElementsApiHelperInterface
from .streamElementsHelperInterface import StreamElementsHelperInterface
from ..exceptions import StreamElementsFailedToCreateDirectoriesException
from ..models.streamElementsFileReference import StreamElementsFileReference
from ..models.streamElementsVoice import StreamElementsVoice
from ..parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ..parser.streamElementsMessageVoiceParserInterface import StreamElementsMessageVoiceParserInterface
from ..settings.streamElementsSettingsRepositoryInterface import StreamElementsSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class StreamElementsHelper(StreamElementsHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        streamElementsApiHelper: StreamElementsApiHelperInterface,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
        streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(streamElementsApiHelper, StreamElementsApiHelperInterface):
            raise TypeError(f'streamElementsApiHelper argument is malformed: \"{streamElementsApiHelper}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(streamElementsMessageVoiceParser, StreamElementsMessageVoiceParserInterface):
            raise TypeError(f'streamElementsMessageVoiceParser argument is malformed: \"{streamElementsMessageVoiceParser}\"')
        elif not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__glacialTtsFileRetriever: Final[GlacialTtsFileRetrieverInterface] = glacialTtsFileRetriever
        self.__streamElementsApiHelper: Final[StreamElementsApiHelperInterface] = streamElementsApiHelper
        self.__streamElementsJsonParser: Final[StreamElementsJsonParserInterface] = streamElementsJsonParser
        self.__streamElementsMessageVoiceParser: Final[StreamElementsMessageVoiceParserInterface] = streamElementsMessageVoiceParser
        self.__streamElementsSettingsRepository: Final[StreamElementsSettingsRepositoryInterface] = streamElementsSettingsRepository
        self.__timber: Final[TimberInterface] = timber

        self.__directoryTreeRegEx: Final[Pattern] = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise StreamElementsFailedToCreateDirectoriesException(f'Failed to create Stream Elements TTS file directories ({filePath=}) ({directoryMatch=})')

        directory = directoryMatch.group(1)

        if await aiofiles.ospath.exists(
            path = directory,
            loop = self.__eventLoop,
        ):
            return

        await aiofiles.os.makedirs(
            name = directory,
            loop = self.__eventLoop,
        )

        self.__timber.log('StreamElementsHelper', f'Created new directories ({filePath=}) ({directory=})')

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None,
    ) -> str | None:
        if not await self.__streamElementsSettingsRepository.useDonationPrefix():
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
        donationPrefix: str | None,
        message: str | None,
        twitchChannelId: str,
        voice: StreamElementsVoice | None,
    ) -> StreamElementsFileReference | None:
        if donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif voice is not None and not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        if voice is None:
            voice = await self.__streamElementsSettingsRepository.getDefaultVoice()

        messageVoiceResult = await self.__streamElementsMessageVoiceParser.determineVoiceFromMessage(message)

        if messageVoiceResult is not None:
            message = messageVoiceResult.message
            voice = messageVoiceResult.voice

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message,
        )

        if not utils.isValidStr(fullMessage):
            return None

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = fullMessage,
            voice = await self.__streamElementsJsonParser.serializeVoice(voice),
            provider = TtsProvider.STREAM_ELEMENTS,
        )

        if glacialFile is not None:
            return StreamElementsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = await self.__streamElementsJsonParser.requireVoice(glacialFile.voice),
            )

        speechBytes = await self.__streamElementsApiHelper.getSpeech(
            message = fullMessage,
            twitchChannelId = twitchChannelId,
            voice = voice,
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = await self.__streamElementsSettingsRepository.getFileExtension(),
            message = fullMessage,
            voice = await self.__streamElementsJsonParser.serializeVoice(voice),
            provider = TtsProvider.STREAM_ELEMENTS,
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath,
        ):
            return StreamElementsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voice = voice,
            )
        else:
            self.__timber.log('StreamElementsHelper', f'Failed to write Stream Elements TTS speechBytes to file ({fullMessage=}) ({glacialFile=})')
            return None

    async def __saveSpeechBytes(
        self,
        speechBytes: bytes,
        fileName: str,
        filePath: str,
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
                loop = self.__eventLoop,
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('StreamElementsHelper', f'Encountered exception when trying to write Stream Elements TTS speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
