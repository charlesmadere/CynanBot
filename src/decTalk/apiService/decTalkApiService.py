import asyncio
import os
import re
import uuid
from asyncio import AbstractEventLoop, CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from dataclasses import dataclass
from typing import ByteString, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
import psutil

from .decTalkApiServiceInterface import DecTalkApiServiceInterface
from ..exceptions import DecTalkExecutableIsMissingException, DecTalkFailedToGenerateSpeechFileException
from ..settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class DecTalkApiService(DecTalkApiServiceInterface):

    @dataclass(frozen = True)
    class FilePaths:
        decTalkPath: str
        fileName: str
        fullFilePath: str
        ttsDirectory: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
        fileExtension: str = 'wav'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__decTalkSettingsRepository: DecTalkSettingsRepositoryInterface = decTalkSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __createTtsDirectory(self, ttsDirectory: str):
        if await aiofiles.ospath.exists(
            path = ttsDirectory,
            loop = self.__eventLoop
        ):
            return

        await aiofiles.os.makedirs(
            name = ttsDirectory,
            loop = self.__eventLoop
        )

        self.__timber.log('DecTalkApiService', f'Created new TTS directory ({ttsDirectory=})')

    async def __generateFilePaths(self) -> FilePaths:
        decTalkPath = await self.__decTalkSettingsRepository.requireDecTalkExecutablePath()

        ttsDirectory = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(TtsProvider.DEC_TALK)
        await self.__createTtsDirectory(ttsDirectory)

        fileName = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
        fileName = f'{fileName}.{self.__fileExtension}'.casefold()

        fullFilePath = f'{ttsDirectory}/{fileName}'

        return DecTalkApiService.FilePaths(
            decTalkPath = os.path.normpath(decTalkPath),
            fileName = os.path.normpath(fileName),
            fullFilePath = os.path.normpath(fullFilePath),
            ttsDirectory = os.path.normpath(ttsDirectory)
        )

    async def generateSpeechFile(self, text: str) -> str:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('DecTalkApiService', f'Generating speech... ({text=})')

        filePaths = await self.__generateFilePaths()

        if not await aiofiles.ospath.exists(
            path = filePaths.decTalkPath,
            loop = self.__eventLoop
        ):
            raise DecTalkExecutableIsMissingException(f'Couldn\'t find DecTalk executable ({filePaths=})')

        decTalkProcess: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        command = f'{filePaths.decTalkPath} -w \"{filePaths.fullFilePath}\" -pre \"[:phone on]\" \"{text}\"'

        try:
            decTalkProcess = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            outputTuple = await asyncio.wait_for(
                fut = decTalkProcess.communicate(),
                timeout = 3
            )
        except BaseException as e:
            exception = e

        outputString: str | None = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('DecTalkApiService', f'Ran DecTalk system command ({command=}) ({outputString=}) ({exception=})')

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killDecTalkProcess(decTalkProcess)

        if not await aiofiles.ospath.exists(
            path = filePaths.fullFilePath,
            loop = self.__eventLoop
        ):
            raise DecTalkFailedToGenerateSpeechFileException(f'Failed to generate speech file ({filePaths=}) ({command=}) ({outputString=}) ({exception=})')

        return filePaths.fullFilePath

    async def __killDecTalkProcess(self, decTalkProcess: Process | None):
        if decTalkProcess is None:
            self.__timber.log('DecTalkApiService', f'Went to kill the DecTalk process, but the process is None ({decTalkProcess=})')
            return
        elif not isinstance(decTalkProcess, Process):
            raise TypeError(f'process argument is malformed: \"{decTalkProcess}\"')
        elif decTalkProcess.returncode is not None:
            self.__timber.log('DecTalkApiService', f'Went to kill a DecTalk process, but the process has a return code ({decTalkProcess=}) ({decTalkProcess.returncode=})')
            return

        self.__timber.log('DecTalkApiService', f'Killing DecTalk process ({decTalkProcess=}) ({decTalkProcess.returncode=})...')
        parent = psutil.Process(decTalkProcess.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__timber.log('DecTalkApiService', f'Finished killing DecTalk process ({decTalkProcess=}) ({decTalkProcess.returncode=}) ({childCount=})')
