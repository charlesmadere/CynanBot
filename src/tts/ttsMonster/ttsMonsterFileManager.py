import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Pattern, Collection

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface


class TtsMonsterFileManager(TtsMonsterFileManagerInterface):

    @dataclass(frozen = True)
    class FetchAndSaveSoundDataTask:
        index: int
        fileName: str
        ttsUrl: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface,
        directory: str = 'temp',
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper
        self.__directory: str = directory
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __fetchTtsSoundData(self, ttsUrl: str) -> bytes:
        if not utils.isValidStr(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        return await self.__ttsMonsterApiService.fetchGeneratedTts(
            ttsUrl = ttsUrl
        )

    async def __generateFileNames(self, size: int) -> FrozenList[str]:
        if not utils.isValidInt(size):
            raise TypeError(f'size argument is malformed: \"{size}\"')
        elif size < 1 or size > utils.getIntMaxSafeSize():
            raise ValueError(f'size argument is out of bounds: {size}')

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileNames: set[str] = set()

        while len(fileNames) < size:
            fileName: str | None = None

            while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
                randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
                fileName = utils.cleanPath(f'{self.__directory}/ttsmonster-{randomUuid}.{self.__fileExtension}')

            fileNames.add(fileName)

        frozenFileNames: FrozenList[str] = FrozenList(fileNames)
        frozenFileNames.freeze()

        return frozenFileNames

    async def saveTtsUrlToNewFile(self, ttsUrl: str) -> str | None:
        if not utils.isValidStr(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        ttsUrls: FrozenList[str] = FrozenList()
        ttsUrls.append(ttsUrl)
        ttsUrls.freeze()

        ttsFileNames = await self.saveTtsUrlsToNewFiles(ttsUrls)

        if ttsFileNames is None or len(ttsFileNames) == 0:
            return None

        return ttsFileNames[0]

    async def saveTtsUrlsToNewFiles(self, ttsUrls: Collection[str]) -> FrozenList[str] | None:
        if not isinstance(ttsUrls, Collection):
            raise TypeError(f'ttsUrls argument is malformed: \"{ttsUrls}\"')

        frozenTtsUrls: FrozenList[str] = FrozenList(ttsUrls)
        frozenTtsUrls.freeze()

        if len(frozenTtsUrls) == 0:
            return None

        fileNames = await self.__generateFileNames(len(frozenTtsUrls))

        for index, ttsUrl in enumerate(frozenTtsUrls):
            soundData = await self.__fetchTtsSoundData(ttsUrl)

            await self.__writeTtsSoundDataToLocalFile(
                soundData = soundData,
                fileName = fileNames[index]
            )

        return fileNames

    async def __writeTtsSoundDataToLocalFile(
        self,
        soundData: bytes,
        fileName: str
    ):
        if not isinstance(soundData, bytes):
            raise TypeError(f'soundData argument is malformed: \"{soundData}\"')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(soundData)
                await file.flush()
        except Exception as e:
            self.__timber.log('TtsMonsterFileManager', f'Encountered exception when trying to write TTS Monster sound to file (\"{fileName}\"): {e}', e, traceback.format_exc())
            raise e

        await self.__ttsTempFileHelper.registerTempFile(fileName)
