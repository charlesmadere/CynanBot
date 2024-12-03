import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class StreamElementsFileManager(StreamElementsFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        directory: str = 'temp',
        fileExtension: str = 'mp3'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__timber: TimberInterface = timber
        self.__directory: str = directory
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __generateFileName(self) -> str:
        fileName: str | None = None

        while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
            randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
            fileName = utils.cleanPath(f'{self.__directory}/streamelements-{randomUuid}.{self.__fileExtension}')

        return fileName

    async def saveSpeechToNewFile(self, speechBytes: bytes) -> str | None:
        if not isinstance(speechBytes, bytes):
            raise TypeError(f'speechBytes argument is malformed: \"{speechBytes}\"')

        fileName = await self.__generateFileName()

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('StreamElementsFileManager', f'Encountered exception when trying to write Stream Elements TTS sound to file (\"{fileName}\"): {e}', e, traceback.format_exc())
            return None

        return fileName
