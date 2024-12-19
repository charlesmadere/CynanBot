import asyncio
from asyncio import CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import ByteString

import aiofiles
import aiofiles.os
import aiofiles.ospath
import psutil

from .decTalkApiServiceInterface import DecTalkApiServiceInterface
from ..exceptions import DecTalkFailedToGenerateSpeechFileException
from ..settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.decTalk.decTalkFileManagerInterface import DecTalkFileManagerInterface


class DecTalkApiService(DecTalkApiServiceInterface):

    def __init__(
        self,
        decTalkFileManager: DecTalkFileManagerInterface,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(decTalkFileManager, DecTalkFileManagerInterface):
            raise TypeError(f'decTalkFileManager argument is malformed: \"{decTalkFileManager}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__decTalkSettingsRepository: DecTalkSettingsRepositoryInterface = decTalkSettingsRepository
        self.__timber: TimberInterface = timber

    async def generateSpeechFile(self, text: str) -> str:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('DecTalkApiService', f'Generating speech... ({text=})')

        pathToDecTalk = await self.__decTalkSettingsRepository.requireDecTalkExecutablePath()

        fileName = await self.__decTalkFileManager.generateNewSpeechFile()
        decTalkProcess: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        command = f'{pathToDecTalk} -w \"{fileName}\" -pre \"[:phone on]\" \"{text}\"'

        try:
            decTalkProcess = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            outputTuple = await asyncio.wait_for(
                fut = decTalkProcess.communicate(),
                timeout = 5
            )
        except BaseException as e:
            exception = e

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killDecTalkProcess(decTalkProcess)
            fileName = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('DecTalkApiService', f'Ran DecTalk system command ({command=}) ({outputString=}) ({exception=})')

        if utils.isValidStr(fileName) and await aiofiles.ospath.exists(fileName) and await aiofiles.ospath.isfile(fileName):
            return fileName
        else:
            raise DecTalkFailedToGenerateSpeechFileException(f'Failed to generate speech file for message: \"{text}\"')

    async def __killDecTalkProcess(self, decTalkProcess: Process | None):
        if decTalkProcess is None:
            self.__timber.log('DecTalkApiService', f'Went to kill the DecTalk process, but the process is None ({decTalkProcess=})')
            return
        elif not isinstance(decTalkProcess, Process):
            raise TypeError(f'process argument is malformed: \"{decTalkProcess}\"')
        elif decTalkProcess.returncode is not None:
            self.__timber.log('DecTalkApiService', f'Went to kill a DecTalk process, but the process has a return code ({decTalkProcess=}) ({decTalkProcess.returncode=})')
            return

        self.__timber.log('DecTalkApiService', f'Killing DecTalk process ({decTalkProcess=})...')
        parent = psutil.Process(decTalkProcess.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__timber.log('DecTalkApiService', f'Finished killing DecTalk process ({decTalkProcess=}) ({childCount=})')
