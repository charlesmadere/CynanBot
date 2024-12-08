import asyncio
import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from typing import Any, Collection, Coroutine, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface


class TtsMonsterFileManager(TtsMonsterFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        directory: str = '../temp',
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__directory: str = directory
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __fetchAndSaveSoundData(
        self,
        index: int,
        fileName: str,
        ttsUrl: str
    ):
        if not utils.isValidInt(index):
            raise TypeError(f'index argument is malformed: \"{index}\"')
        elif index < 0 or index > utils.getIntMaxSafeSize():
            raise ValueError(f'index argument is out of bounds: {index}')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')
        elif not utils.isValidStr(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        soundData = await self.__ttsMonsterApiService.fetchGeneratedTts(ttsUrl)

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
        if not utils.isValidUrl(ttsUrl):
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

        frozenTtsUrls: FrozenList[str] = FrozenList()

        for index, ttsUrl in enumerate(ttsUrls):
            if not utils.isValidUrl(ttsUrl):
                raise TypeError(f'Encountered bad TTS URL at index {index}: \"{ttsUrl}\"')

            frozenTtsUrls.append(ttsUrl)

        frozenTtsUrls.freeze()

        if len(frozenTtsUrls) == 0:
            return None

        fileNames = await self.__generateFileNames(len(frozenTtsUrls))
        fetchAndSaveCoroutines: list[Coroutine[Any, Any, Any]] = list()

        for index in range(len(frozenTtsUrls)):
            fetchAndSaveCoroutines.append(self.__fetchAndSaveSoundData(
                index = index,
                fileName = fileNames[index],
                ttsUrl = frozenTtsUrls[index]
            ))

        try:
            await asyncio.gather(*fetchAndSaveCoroutines, return_exceptions = True)
        except Exception as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered unknown error when fetching and saving TTS files ({ttsUrls=}): {e}', e, traceback.format_exc())
            return None

        return fileNames
