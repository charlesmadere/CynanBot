import os
import traceback
from datetime import datetime, timedelta, timezone, tzinfo

import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.tempFileHelper.ttsTempFile import TtsTempFile
from CynanBot.tts.tempFileHelper.ttsTempFileHelperInterface import \
    TtsTempFileHelperInterface


class TtsTempFileHelper(TtsTempFileHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeToLive: timedelta = timedelta(minutes = 10),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeToLive, timedelta):
            raise TypeError(f'timeToLive argument is malformed: \"{timeToLive}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: TimberInterface = timber
        self.__timeToLive: timedelta = timeToLive
        self.__timeZone: tzinfo = timeZone

        self.__tempFiles: list[TtsTempFile] = list()

    async def deleteOldTempFiles(self):
        tempFiles = await self.__getOldTempFiles()

        if tempFiles is None or len(tempFiles) == 0:
            return

        tempFileSize = len(tempFiles)
        self.__timber.log('TtsTempFileHelper', f'Deleting {tempFileSize} temp file(s)...')

        for tempFile in tempFiles:
            await self.__removeFile(tempFile.getFileName())

        self.__timber.log('TtsTempFileHelper', f'Finished deleting {tempFileSize} temp file(s)')

    async def __getOldTempFiles(self) -> list[TtsTempFile]:
        oldTempFiles: list[TtsTempFile] = list()
        now = datetime.now(self.__timeZone)

        for tempFile in self.__tempFiles:
            if (tempFile.getCreationDateTime() + self.__timeToLive) >= now:
                oldTempFiles.append(tempFile)

        return oldTempFiles

    async def registerTempFile(self, fileName: str | None):
        if fileName is not None and not isinstance(fileName, str):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')
        elif not utils.isValidStr(fileName):
            return

        if not await aiofiles.ospath.exists(fileName):
            self.__timber.log('TtsTempFileHelper', f'Attempted to register temporary file \"{fileName}\" but it doesn\'t exist')
            return

        now = datetime.now(self.__timeZone)

        self.__tempFiles.append(TtsTempFile(
            creationDateTime = now,
            fileName = fileName
        ))

    async def __removeFile(self, fileName: str) -> bool:
        try:
            os.remove(fileName)
            return True
        except Exception as e:
            self.__timber.log('TtsTempFileHelper', f'Failed to remove temporary file \"{fileName}\": {e}', e, traceback.format_exc())
            return False
