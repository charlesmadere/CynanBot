import asyncio
import traceback
from asyncio import AbstractEventLoop
from typing import Any, Collection, Coroutine

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from ...misc import utils as utils
from ...storage.tempFileHelperInterface import TempFileHelperInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface


class TtsMonsterFileManager(TtsMonsterFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        tempFileHelper: TempFileHelperInterface,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(tempFileHelper, TempFileHelperInterface):
            raise TypeError(f'tempFileHelper argument is malformed: \"{tempFileHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__tempFileHelper: TempFileHelperInterface = tempFileHelper
        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__fileExtension: str = fileExtension

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

        fileNames = await self.__tempFileHelper.getTempFileNames(
            amount = len(frozenTtsUrls),
            prefix = 'ttsmonster',
            extension = self.__fileExtension
        )

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
