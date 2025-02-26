import re
import traceback
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..exceptions import TtsMonsterFailedToCreateDirectoriesException
from ..messageChunkParser.ttsMonsterMessageChunkParserInterface import TtsMonsterMessageChunkParserInterface
from ..models.ttsMonsterFileReference import TtsMonsterFileReference
from ..models.ttsMonsterMessageChunk import TtsMonsterMessageChunk
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ..settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class TtsMonsterHelper(TtsMonsterHelperInterface):

    @dataclass(frozen = True)
    class MessageVoices:
        messageChunks: FrozenList[TtsMonsterMessageChunk] | None
        allVoices: frozenset[TtsMonsterVoice]
        primaryVoice: TtsMonsterVoice

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        timber: TimberInterface,
        ttsMonsterMessageChunkParser: TtsMonsterMessageChunkParserInterface,
        ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterMessageChunkParser, TtsMonsterMessageChunkParserInterface):
            raise TypeError(f'ttsMonsterMessageChunkParser argument is malformed: \"{ttsMonsterMessageChunkParser}\"')
        elif not isinstance(ttsMonsterPrivateApiHelper, TtsMonsterPrivateApiHelperInterface):
            raise TypeError(f'ttsMonsterPrivateApiHelper argument is malformed: \"{ttsMonsterPrivateApiHelper}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__timber: TimberInterface = timber
        self.__ttsMonsterMessageChunkParser: TtsMonsterMessageChunkParserInterface = ttsMonsterMessageChunkParser
        self.__ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface = ttsMonsterPrivateApiHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository

        self.__directoryTreeRegEx: Pattern = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise TtsMonsterFailedToCreateDirectoriesException(f'Failed to create TTS Monster file directories ({filePath=}) ({directoryMatch=})')

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

        self.__timber.log('TtsMonsterHelper', f'Created new directories ({directory=})')

    async def __determineMessageVoices(self, message: str) -> MessageVoices:
        messageChunks = await self.__ttsMonsterMessageChunkParser.parse(
            message = message,
            defaultVoice = await self.__ttsMonsterSettingsRepository.getDefaultVoice()
        )

        allVoices: set[TtsMonsterVoice] = set()
        primaryVoice: TtsMonsterVoice

        if messageChunks is not None and len(messageChunks) >= 1:
            for messageChunk in messageChunks:
                allVoices.add(messageChunk.voice)

            primaryVoice = messageChunks[0].voice
        else:
            primaryVoice = await self.__ttsMonsterSettingsRepository.getDefaultVoice()

        return TtsMonsterHelper.MessageVoices(
            messageChunks = messageChunks,
            allVoices = frozenset(allVoices),
            primaryVoice = primaryVoice
        )

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            extraConfigurationData = None,
            message = message,
            provider = TtsProvider.TTS_MONSTER
        )

        messageVoices = await self.__determineMessageVoices(message)

        if glacialFile is not None:
            return TtsMonsterFileReference(
                storeDateTime = glacialFile.storeDateTime,
                allVoices = messageVoices.allVoices,
                filePath = glacialFile.filePath,
                primaryVoice = messageVoices.primaryVoice
            )

        speechBytes = await self.__ttsMonsterPrivateApiHelper.getSpeech(
            message = message,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            extraConfigurationData = None,
            fileExtension = await self.__ttsMonsterSettingsRepository.getFileExtension(),
            message = message,
            provider = TtsProvider.TTS_MONSTER
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath
        ):
            return TtsMonsterFileReference(
                storeDateTime = glacialFile.storeDateTime,
                allVoices = messageVoices.allVoices,
                filePath = glacialFile.filePath,
                primaryVoice = messageVoices.primaryVoice
            )
        else:
            self.__timber.log('TtsMonsterHelper', f'Failed to write TTS Monster speechBytes to file ({message=}) ({glacialFile=})')
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
            self.__timber.log('TtsMonsterHelper', f'Encountered exception when trying to write TTS Monster speechBytes to file ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
