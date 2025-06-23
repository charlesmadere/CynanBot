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
from ..models.ttsMonsterDonationPrefixConfig import TtsMonsterDonationPrefixConfig
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

        self.__timber.log('TtsMonsterHelper', f'Created new directories ({filePath=}) ({directory=})')

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None
    ) -> str | None:
        donationPrefixConfig = await self.__ttsMonsterSettingsRepository.getDonationPrefixConfig()

        match donationPrefixConfig:
            case TtsMonsterDonationPrefixConfig.DISABLED:
                if utils.isValidStr(message):
                    return message
                else:
                    return None

            case TtsMonsterDonationPrefixConfig.ENABLED:
                if utils.isValidStr(donationPrefix) and utils.isValidStr(message):
                    return f'{donationPrefix} {message}'
                elif utils.isValidStr(donationPrefix):
                    return donationPrefix
                elif utils.isValidStr(message):
                    return message
                else:
                    return None

            case TtsMonsterDonationPrefixConfig.IF_MESSAGE_IS_BLANK:
                if utils.isValidStr(message):
                    return message
                elif utils.isValidStr(donationPrefix):
                    return donationPrefix
                else:
                    return None

            case _:
                raise RuntimeError(f'Encountered unknown TtsMonsterDonationPrefixConfig value: \"{donationPrefixConfig}\"')

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
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
        voice: TtsMonsterVoice | None
    ) -> TtsMonsterFileReference | None:
        if donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif voice is not None and not isinstance(voice, TtsMonsterVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message
        )

        if not utils.isValidStr(fullMessage):
            return None

        if voice is not None:
            fullMessage = f'{voice.inMessageName}: {fullMessage}'

        messageVoices = await self.__determineMessageVoices(fullMessage)

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = fullMessage,
            voice = None,
            provider = TtsProvider.TTS_MONSTER
        )

        if glacialFile is not None:
            return TtsMonsterFileReference(
                storeDateTime = glacialFile.storeDateTime,
                allVoices = messageVoices.allVoices,
                filePath = glacialFile.filePath,
                primaryVoice = messageVoices.primaryVoice
            )

        speechBytes = await self.__ttsMonsterPrivateApiHelper.getSpeech(
            message = fullMessage,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = await self.__ttsMonsterSettingsRepository.getFileExtension(),
            message = fullMessage,
            voice = None,
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
            self.__timber.log('TtsMonsterHelper', f'Failed to write TTS Monster speechBytes to file ({fullMessage=}) ({glacialFile=})')
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
            self.__timber.log('TtsMonsterHelper', f'Encountered exception when trying to write TTS Monster speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
