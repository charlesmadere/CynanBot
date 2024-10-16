import os
import traceback
from datetime import datetime, timedelta
from typing import Collection

import aiofiles.ospath
from frozenlist import FrozenList

from .ttsTempFile import TtsTempFile
from .ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsTempFileHelper(TtsTempFileHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        maxDeletionAttempts: int = 3,
        timeToLive: timedelta = timedelta(minutes = 15)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(maxDeletionAttempts):
            raise TypeError(f'maxDeletionAttempts argument is malformed: \"{maxDeletionAttempts}\"')
        elif maxDeletionAttempts < 1 or maxDeletionAttempts > utils.getIntMaxSafeSize():
            raise ValueError(f'maxDeletionAttempts argument is out of bounds: {maxDeletionAttempts}')
        elif not isinstance(timeToLive, timedelta):
            raise TypeError(f'timeToLive argument is malformed: \"{timeToLive}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__maxDeletionAttempts: int = maxDeletionAttempts
        self.__timeToLive: timedelta = timeToLive

        self.__tempFiles: list[TtsTempFile] = list()

    async def deleteOldTempFiles(self):
        tempFilesToDelete = await self.__getTempFilesToDelete()

        if len(tempFilesToDelete) == 0:
            return

        tempFilesToDeleteSize = len(tempFilesToDelete)
        self.__timber.log('TtsTempFileHelper', f'Deleting {tempFilesToDeleteSize} temp file(s)...')

        successes = 0
        fails = 0
        deleteRetries: list[TtsTempFile] = list()

        for tempFile in tempFilesToDelete:
            if await self.__removeFile(tempFile.fileName):
                successes = successes + 1
            else:
                tempFile.incrementDeletionAttempts()
                fails = fails + 1
                deleteRetries.append(tempFile)

        if len(deleteRetries) >= 1:
            self.__tempFiles.extend(deleteRetries)

        self.__timber.log('TtsTempFileHelper', f'Finished deleting {tempFilesToDeleteSize} temp file(s) ({successes=}) ({fails=})')

    async def __getTempFilesToDelete(self) -> list[TtsTempFile]:
        tempFilesToDrop: list[TtsTempFile] = list()
        tempFilesToDelete: list[TtsTempFile] = list()
        now = datetime.now(self.__timeZoneRepository.getDefault())

        for tempFile in self.__tempFiles:
            if tempFile.deletionAttempts > self.__maxDeletionAttempts:
                tempFilesToDrop.append(tempFile)
            elif (tempFile.creationDateTime + self.__timeToLive) <= now:
                tempFilesToDelete.append(tempFile)

        for tempFileToDrop in tempFilesToDrop:
            self.__tempFiles.remove(tempFileToDrop)

        for tempFileToDelete in tempFilesToDelete:
            self.__tempFiles.remove(tempFileToDelete)

        return tempFilesToDelete

    async def registerTempFile(self, fileName: str | None):
        if fileName is not None and not isinstance(fileName, str):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')
        elif not utils.isValidStr(fileName):
            return

        if not await aiofiles.ospath.exists(fileName):
            self.__timber.log('TtsTempFileHelper', f'Attempted to register temporary file \"{fileName}\" but it doesn\'t exist')
            return

        now = datetime.now(self.__timeZoneRepository.getDefault())

        self.__tempFiles.append(TtsTempFile(
            creationDateTime = now,
            fileName = fileName
        ))

    async def registerTempFiles(self, fileNames: Collection[str]):
        if not isinstance(fileNames, Collection):
            raise TypeError(f'fileNames argument is malformed: \"{fileNames}\"')

        frozenFileNames: FrozenList[str] = FrozenList(fileNames)
        frozenFileNames.freeze()

        if len(frozenFileNames) == 0:
            return

        for fileName in frozenFileNames:
            await self.registerTempFile(fileName)

    async def __removeFile(self, fileName: str) -> bool:
        if not await aiofiles.ospath.exists(fileName):
            self.__timber.log('TtsTempFileHelper', f'No need to remove temporary file \"{fileName}\" as it does not exist')
            return True

        try:
            os.remove(fileName)
            return True
        except Exception as e:
            self.__timber.log('TtsTempFileHelper', f'Failed to remove temporary file \"{fileName}\": {e}', e, traceback.format_exc())
            return False
