import traceback
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .microsoftSamFileManagerInterface import MicrosoftSamFileManagerInterface
from ...misc import utils as utils
from ...storage.tempFileHelperInterface import TempFileHelperInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftSamFileManager(MicrosoftSamFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        tempFileHelper: TempFileHelperInterface,
        timber: TimberInterface,
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(tempFileHelper, TempFileHelperInterface):
            raise TypeError(f'tempFileHelper argument is malformed: \"{tempFileHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__tempFileHelper: TempFileHelperInterface = tempFileHelper
        self.__timber: TimberInterface = timber
        self.__fileExtension: str = fileExtension

    async def saveSpeechToNewFile(self, speechBytes: bytes) -> str | None:
        if not isinstance(speechBytes, bytes):
            raise TypeError(f'speechBytes argument is malformed: \"{speechBytes}\"')

        fileName = await self.__tempFileHelper.getTempFileName(
            prefix = 'microsoftsam',
            extension = self.__fileExtension
        )

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('MicrosoftSamFileManager', f'Encountered exception when trying to write Stream Elements TTS sound to file (\"{fileName}\"): {e}', e, traceback.format_exc())
            return None

        return fileName
