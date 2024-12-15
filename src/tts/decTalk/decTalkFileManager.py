import traceback
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .decTalkFileManagerInterface import DecTalkFileManagerInterface
from ...misc import utils as utils
from ...storage.tempFileHelperInterface import TempFileHelperInterface
from ...timber.timberInterface import TimberInterface


class DecTalkFileManager(DecTalkFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        tempFileHelper: TempFileHelperInterface,
        timber: TimberInterface,
        extension: str = 'txt'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(tempFileHelper, TempFileHelperInterface):
            raise TypeError(f'tempFileHelper argument is malformed: \"{tempFileHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(extension):
            raise TypeError(f'extension argument is malformed: \"{extension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__tempFileHelper: TempFileHelperInterface = tempFileHelper
        self.__timber: TimberInterface = timber
        self.__extension: str = extension

    async def writeCommandToNewFile(self, command: str) -> str | None:
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')

        fileName = await self.__tempFileHelper.getTempFileName(
            prefix = 'dectalk',
            extension = self.__extension
        )

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'w',
                encoding = 'windows-1252', # DECTalk requires Windows-1252 encoding
                loop = self.__eventLoop
            ) as file:
                await file.write(command)
                await file.flush()
        except Exception as e:
            self.__timber.log('DecTalkFileManager', f'Encountered exception when trying to write command to TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())
            return None

        return fileName
