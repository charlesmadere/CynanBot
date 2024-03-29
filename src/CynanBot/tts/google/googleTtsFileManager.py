import base64
import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface


class GoogleTtsFileManager(GoogleTtsFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        directory: str = 'temp'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__timber: TimberInterface = timber
        self.__directory: str = utils.cleanPath(directory)

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __decodeBase64Command(self, base64Command: str | None) -> bytes | None:
        if base64Command is None:
            return None
        elif not isinstance(base64Command, str):
            raise TypeError(f'base64Command argument is malformed: \"{base64Command}\"')
        elif not utils.isValidStr(base64Command):
            return None

        decoded = base64.b64decode(
            s = base64Command,
            validate = True
        )

        if decoded is None or len(decoded) == 0:
            self.__timber.log('GoogleTtsFileManager', f'Unable to decode base64Command into bytes ({decoded=})')
            return None

        return decoded

    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        if not utils.isValidStr(base64Command):
            raise TypeError(f'base64Command argument is malformed: \"{base64Command}\"')

        decoded = await self.__decodeBase64Command(base64Command)

        if decoded is None:
            self.__timber.log('GoogleTtsFileManager', f'Unable to decode base64Command ({base64Command=})')
            return None

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileName: str | None = None

        while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
            randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
            fileName = utils.cleanPath(f'{self.__directory}/google-{randomUuid}.mp3')

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(decoded)
                await file.flush()
        except Exception as e:
            self.__timber.log('GoogleTtsFileManager', f'Encountered exception when trying to write command to TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())
            fileName = None

        return fileName
