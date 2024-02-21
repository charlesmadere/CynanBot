import os
import re
import traceback
import uuid
from typing import Optional, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkFileManagerInterface import \
    DecTalkFileManagerInterface


class DecTalkFileManager(DecTalkFileManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: TimberInterface,
        directory: str = 'temp'
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidStr(directory):
            raise ValueError(f'directory argument is malformed: \"{directory}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__directory: str = utils.cleanStr(directory)

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def deleteFile(self, fileName: Optional[str]):
        if not utils.isValidStr(fileName):
            return
        elif not await aiofiles.ospath.exists(fileName):
            return

        try:
            os.remove(fileName)
        except Exception as e:
            self.__timber.log('DecTalkFileManager', f'Unable to delete TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())

    async def writeCommandToNewFile(self, command: str) -> Optional[str]:
        if not utils.isValidStr(command):
            raise ValueError(f'command argument is malformed: \"{command}\"')

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileName: Optional[str] = None

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
        except Exception as e:
            self.__timber.log('DecTalkFileManager', f'Encountered exception when trying to write command to TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())
            fileName = None

        return fileName
