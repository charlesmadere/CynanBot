import re
import traceback
import uuid
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkFileManagerInterface import \
    DecTalkFileManagerInterface


class DecTalkFileManager(DecTalkFileManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        directory: str = 'temp'
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__directory: str = utils.cleanPath(directory)

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def writeCommandToNewFile(self, command: str) -> str | None:
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileName: str | None = None

        while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
            randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
            fileName = utils.cleanPath(f'{self.__directory}/dectalk-{randomUuid}.txt')

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'w',
                encoding = 'windows-1252', # DECTalk requires Windows-1252 encoding
                loop = self.__backgroundTaskHelper.getEventLoop()
            ) as file:
                await file.write(command)
                await file.flush()
        except Exception as e:
            self.__timber.log('DecTalkFileManager', f'Encountered exception when trying to write command to TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())
            fileName = None

        return fileName
