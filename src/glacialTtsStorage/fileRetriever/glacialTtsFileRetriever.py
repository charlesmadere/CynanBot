import re
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Final, Pattern

import aiofiles.os
import aiofiles.ospath

from .glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ..exceptions import GlacialTtsFolderIsNotAFolder
from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ..repository.glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsFileRetriever(GlacialTtsFileRetrieverInterface):

    @dataclass(frozen = True, slots = True)
    class FileReference:
        fileName: str
        filePath: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsStorageRepository: GlacialTtsStorageRepositoryInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsStorageRepository, GlacialTtsStorageRepositoryInterface):
            raise TypeError(f'glacialTtsStorageRepository argument is malformed: \"{glacialTtsStorageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__glacialTtsStorageRepository: Final[GlacialTtsStorageRepositoryInterface] = glacialTtsStorageRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsDirectoryProvider: Final[TtsDirectoryProviderInterface] = ttsDirectoryProvider

        self.__fileNameWithoutExtensionRegEx: Final[Pattern] = re.compile(r'^(\w+)\.\w+$', re.IGNORECASE)

    async def findFile(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif voice is not None and not isinstance(voice, str):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.__glacialTtsStorageRepository.get(
            message = message,
            voice = voice,
            provider = provider,
        )

        if glacialTtsData is None:
            return None

        fileReference = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider,
        )

        if fileReference is None:
            return None

        self.__timber.log('GlacialTtsFileRetriever', f'Found a Glacial TTS file to reuse ({glacialTtsData=}) ({fileReference=})')

        return GlacialTtsFileReference(
            glacialTtsData = glacialTtsData,
            fileName = fileReference.fileName,
            filePath = fileReference.filePath,
        )

    async def __findFile(
        self,
        glacialId: str,
        provider: TtsProvider,
    ) -> FileReference | None:
        providerFolder = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(provider)

        if not await aiofiles.ospath.exists(
            path = providerFolder,
            loop = self.__eventLoop,
        ):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder does not exist ({glacialId=}) ({providerFolder=})')
            return None
        elif not await aiofiles.ospath.isdir(
            s = providerFolder,
            loop = self.__eventLoop,
        ):
            self.__timber.log('GlacialTtsFileRetriever', f'A glacial ID exists for the given TTS, but its folder is not a directory ({glacialId=}) ({providerFolder=})')
            raise GlacialTtsFolderIsNotAFolder(f'A glacial ID exists for the given TTS, but its folder is not a directory ({glacialId=}) ({providerFolder=})')

        directoryContents = await aiofiles.os.scandir(
            path = providerFolder,
            loop = self.__eventLoop,
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
                    filePath = f'{providerFolder}/{entry.name}',
                )

        return None

    async def saveFile(
        self,
        fileExtension: str,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference:
        if not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif voice is not None and not isinstance(voice, str):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.__glacialTtsStorageRepository.add(
            message = message,
            voice = voice,
            provider = provider,
        )

        glacialTtsFileReference = await self.__findFile(
            glacialId = glacialTtsData.glacialId,
            provider = provider,
        )

        if glacialTtsFileReference is not None:
            self.__timber.log('GlacialTtsFileRetriever', f'Clobbering a TTS file that already exists for the given arguments ({fileExtension=}) ({message=}) ({voice=}) ({provider=}) ({glacialTtsData=}) ({glacialTtsFileReference=})')

        providerFolder = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(provider)
        fileName = f'{glacialTtsData.glacialId}.{fileExtension}'
        filePath = f'{providerFolder}/{fileName}'

        return GlacialTtsFileReference(
            glacialTtsData = glacialTtsData,
            fileName = fileName,
            filePath = filePath,
        )
