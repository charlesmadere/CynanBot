import re
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Pattern

import aiofiles.os
import aiofiles.ospath

from .glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ..exceptions import GlacialTtsAlreadyExists, GlacialTtsFolderIsNotAFolder
from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ..repository.glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.ttsProvider import TtsProvider


class GlacialTtsFileRetriever(GlacialTtsFileRetrieverInterface):

    @dataclass(frozen = True)
    class FileReference:
        fileName: str
        filePath: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsStorageRepository, GlacialTtsStorageRepositoryInterface):
            raise TypeError(f'glacialTtsStorageRepository argument is malformed: \"{glacialTtsStorageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface = glacialTtsStorageRepository
        self.__timber: TimberInterface = timber
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider

        self.__fileNameWithoutExtensionRegEx: Pattern = re.compile(r'^(\w+)\.\w+$', re.IGNORECASE)

    async def findFile(
        self,
        extraConfigurationData: str | None,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference | None:
        if extraConfigurationData is not None and not isinstance(extraConfigurationData, str):
            raise TypeError(f'extraConfigurationData argument is malformed: \"{extraConfigurationData}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.__glacialTtsStorageRepository.get(
            extraConfigurationData = extraConfigurationData,
            message = message,
            provider = provider
        )

        if glacialTtsData is None:
            return None

        fileReference = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider
        )

        if fileReference is None:
            return None
        else:
            self.__timber.log('GlacialTtsFileRetriever', f'Found a Glacial TTS file to reuse ({glacialTtsData=}) ({fileReference=})')

            return GlacialTtsFileReference(
                glacialTtsData = glacialTtsData,
                fileName = fileReference.fileName,
                filePath = fileReference.filePath
            )

    async def __findFile(
        self,
        glacialId: str,
        provider: TtsProvider
    ) -> FileReference | None:
        providerFolder = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(provider)

        if not await aiofiles.ospath.exists(providerFolder):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder does not exist ({glacialId=}) ({providerFolder=})')
            return None
        elif not await aiofiles.ospath.isdir(providerFolder):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder is not a directory ({glacialId=}) ({providerFolder=})')
            raise GlacialTtsFolderIsNotAFolder(f'A glacial ID exists for the given TTS, but its folder is not a directory ({glacialId=}) ({providerFolder=})')

        directoryContents = await aiofiles.os.scandir(
            path = providerFolder,
            loop = self.__eventLoop
        )

        for entry in directoryContents:
            if not entry.is_file():
                continue

            fileNameWithoutExtensionMatch = self.__fileNameWithoutExtensionRegEx.fullmatch(entry.name)
            if fileNameWithoutExtensionMatch is None:
                continue

            fileNameWithoutExtension = fileNameWithoutExtensionMatch.group(1)
            if not utils.isValidStr(fileNameWithoutExtension):
                continue

            if glacialId == fileNameWithoutExtension:
                return GlacialTtsFileRetriever.FileReference(
                    fileName = entry.name,
                    filePath = f'{providerFolder}/{entry.name}'
                )

        return None

    async def saveFile(
        self,
        extraConfigurationData: str | None,
        fileExtension: str,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference:
        if extraConfigurationData is not None and not isinstance(extraConfigurationData, str):
            raise TypeError(f'extraConfigurationData argument is malformed: \"{extraConfigurationData}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.__glacialTtsStorageRepository.get(
            extraConfigurationData = extraConfigurationData,
            message = message,
            provider = provider
        )

        if glacialTtsData is not None:
            raise GlacialTtsAlreadyExists(f'A Glacial TTS file already exists for the given data ({message=}) ({provider=}) ({glacialTtsData=})')

        glacialTtsData = await self.__glacialTtsStorageRepository.add(
            extraConfigurationData = extraConfigurationData,
            message = message,
            provider = provider
        )

        fileReference = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider
        )

        if fileReference is not None:
            raise GlacialTtsAlreadyExists(f'A Glacial TTS file already exists for the given data ({message=}) ({provider=}) ({fileReference=})')

        providerFolder = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(provider)
        fileName = f'{glacialTtsData.glacialId}.{fileExtension}'
        filePath = f'{providerFolder}/{fileName}'

        return GlacialTtsFileReference(
            glacialTtsData = glacialTtsData,
            fileName = fileName,
            filePath = filePath
        )
