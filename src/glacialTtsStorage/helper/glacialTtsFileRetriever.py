import re
from typing import Pattern

import aiofiles.os
import aiofiles.ospath
from asyncio import AbstractEventLoop

from .glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ..exceptions import GlacialTtsAlreadyExists
from ..mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ..repository.glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.ttsProvider import TtsProvider


class GlacialTtsFileRetriever(GlacialTtsFileRetrieverInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsDataMapper: GlacialTtsDataMapperInterface,
        glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface,
        timber: TimberInterface,
        directory: str = '../tts'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsDataMapper, GlacialTtsDataMapperInterface):
            raise TypeError(f'glacialTtsDataMapper argument is malformed: \"{glacialTtsDataMapper}\"')
        elif not isinstance(glacialTtsStorageRepository, GlacialTtsStorageRepositoryInterface):
            raise TypeError(f'glacialTtsStorageRepository argument is malformed: \"{glacialTtsStorageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsDataMapper: GlacialTtsDataMapperInterface = glacialTtsDataMapper
        self.__glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface = glacialTtsStorageRepository
        self.__timber: TimberInterface = timber
        self.__directory: str = utils.cleanPath(directory)

        self.__fileNameWithoutExtensionRegEx: Pattern = re.compile(r'^(\w+)\.\w+$', re.IGNORECASE)

    async def findFile(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.__glacialTtsStorageRepository.get(
            message = message,
            provider = provider
        )

        if glacialTtsData is None:
            return None

        filePath = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider
        )

        if not utils.isValidStr(filePath):
            return None

        self.__timber.log('GlacialTtsFileRetriever', f'Found a Glacial TTS file to reuse ({glacialTtsData=}) ({filePath=})')

        return GlacialTtsFileReference(
            glacialTtsData = glacialTtsData,
            filePath = filePath
        )

    async def __findFile(
        self,
        glacialId: str,
        provider: TtsProvider
    ) -> str | None:
        providerFolder = await self.__glacialTtsDataMapper.toFolderName(provider)
        currentTtsFolder = f'{self.__directory}/{providerFolder}'

        if not await aiofiles.ospath.exists(currentTtsFolder):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder does not exist ({glacialId=}) ({currentTtsFolder=})')
            return None
        elif not await aiofiles.ospath.isdir(currentTtsFolder):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder is not a directory ({glacialId=}) ({currentTtsFolder=})')
            return None

        directoryContents = await aiofiles.os.scandir(currentTtsFolder)

        for entry in directoryContents:
            if not entry.is_file():
                continue

            fileNameWithoutExtensionMatch = self.__fileNameWithoutExtensionRegEx.fullmatch(entry.name)

            if fileNameWithoutExtensionMatch is None:
                continue

            fileNameWithoutExtension = fileNameWithoutExtensionMatch.group(1)

            if glacialId == fileNameWithoutExtension:
                return f'{currentTtsFolder}/{entry.name}'

        return None

    async def saveFile(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference:
        glacialTtsData = await self.__glacialTtsStorageRepository.get(
            message = message,
            provider = provider
        )

        if glacialTtsData is not None:
            raise GlacialTtsAlreadyExists(f'A Glacial TTS file already exists for the given data ({message=}) ({provider=}) ({glacialTtsData=})')

        glacialTtsData = await self.__glacialTtsStorageRepository.add(
            message = message,
            provider = provider
        )

        filePath = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider
        )

        if utils.isValidStr(filePath):
            raise GlacialTtsAlreadyExists(f'A Glacial TTS file already exists for the given data ({message=}) ({provider=}) ({filePath=})')

        providerFolder = await self.__glacialTtsDataMapper.toFolderName(provider)
        filePath = f'{self.__directory}/{providerFolder}/{glacialTtsData.glacialId}'

        return GlacialTtsFileReference(
            glacialTtsData = glacialTtsData,
            filePath = filePath
        )
