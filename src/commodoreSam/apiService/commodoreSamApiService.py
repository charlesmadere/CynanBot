import asyncio
import os
import re
import uuid
from asyncio import AbstractEventLoop, CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from dataclasses import dataclass
from typing import ByteString, Final, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
import psutil

from .commodoreSamApiServiceInterface import CommodoreSamApiServiceInterface
from ..exceptions import CommodoreSamExecutableIsMissingException, CommodoreSamFailedToGenerateSpeechFileException
from ..settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class CommodoreSamApiService(CommodoreSamApiServiceInterface):

    @dataclass(frozen = True)
    class CommodoreSamArguments:
        mouth: int | None
        pitch: int | None
        speed: int | None
        throat: int | None
        fullArgumentString: str

    @dataclass(frozen = True)
    class FilePaths:
        commodoreSamPath: str
        fileName: str
        fullFilePath: str
        ttsDirectory: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
        fileExtension: str = 'wav',
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(commodoreSamSettingsRepository, CommodoreSamSettingsRepositoryInterface):
            raise TypeError(f'commodoreSamSettingsRepository argument is malformed: \"{commodoreSamSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__commodoreSamSettingsRepository: Final[CommodoreSamSettingsRepositoryInterface] = commodoreSamSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsDirectoryProvider: Final[TtsDirectoryProviderInterface] = ttsDirectoryProvider
        self.__fileExtension: Final[str] = fileExtension

        self.__fileNameRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __createTtsDirectory(self, ttsDirectory: str):
        if await aiofiles.ospath.exists(
            path = ttsDirectory,
            loop = self.__eventLoop,
        ):
            return

        await aiofiles.os.makedirs(
            name = ttsDirectory,
            loop = self.__eventLoop,
        )

        self.__timber.log('CommodoreSamApiService', f'Created new TTS directory ({ttsDirectory=})')

    async def __fetchCommodoreSamArguments(self) -> CommodoreSamArguments:
        mouth = await self.__commodoreSamSettingsRepository.getMouthParameter()
        pitch = await self.__commodoreSamSettingsRepository.getPitchParameter()
        speed = await self.__commodoreSamSettingsRepository.getSpeedParameter()
        throat = await self.__commodoreSamSettingsRepository.getThroatParameter()

        fullArgumentString = ''

        if mouth is not None:
            fullArgumentString = fullArgumentString + f'-mouth {mouth} '

        if pitch is not None:
            fullArgumentString = fullArgumentString + f'-pitch {pitch} '

        if speed is not None:
            fullArgumentString = fullArgumentString + f'-speed {speed} '

        if throat is not None:
            fullArgumentString = fullArgumentString + f'-throat {throat} '

        return CommodoreSamApiService.CommodoreSamArguments(
            mouth = mouth,
            pitch = pitch,
            speed = speed,
            throat = throat,
            fullArgumentString = fullArgumentString.strip(),
        )

    async def __generateFilePaths(self) -> FilePaths:
        commodoreSamPath = await self.__commodoreSamSettingsRepository.requireCommodoreSamExecutablePath()

        ttsDirectory = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(TtsProvider.COMMODORE_SAM)
        await self.__createTtsDirectory(ttsDirectory)

        fileName = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
        fileName = f'{fileName}.{self.__fileExtension}'.casefold()

        fullFilePath = f'{ttsDirectory}/{fileName}'

        return CommodoreSamApiService.FilePaths(
            commodoreSamPath = os.path.normpath(commodoreSamPath),
            fileName = os.path.normpath(fileName),
            fullFilePath = os.path.normpath(fullFilePath),
            ttsDirectory = os.path.normpath(ttsDirectory),
        )

    async def generateSpeechFile(self, text: str) -> str:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('CommodoreSamApiService', f'Generating speech... ({text=})')

        filePaths = await self.__generateFilePaths()

        if not await aiofiles.ospath.isfile(
            path = filePaths.commodoreSamPath,
            loop = self.__eventLoop,
        ):
            raise CommodoreSamExecutableIsMissingException(f'Couldn\'t find Commodore SAM executable ({filePaths=})')

        commodoreSamArguments = await self.__fetchCommodoreSamArguments()
        command = f'{filePaths.commodoreSamPath} -wav \"{filePaths.fullFilePath}\" {commodoreSamArguments.fullArgumentString} {text}'

        commodoreSamProcess: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        try:
            commodoreSamProcess = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE,
            )

            outputTuple = await asyncio.wait_for(
                fut = commodoreSamProcess.communicate(),
                timeout = 3,
            )
        except BaseException as e:
            exception = e

        outputString: str | None = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        textLength = len(text)
        commandLength = len(command)

        self.__timber.log('CommodoreSamApiService', f'Ran Commodore SAM system command ({textLength=}) ({commandLength=}) ({command=}) ({outputString=}) ({exception=})')

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killCommodoreSamProcess(commodoreSamProcess)

        if not await aiofiles.ospath.isfile(
            path = filePaths.fullFilePath,
            loop = self.__eventLoop,
        ):
            raise CommodoreSamFailedToGenerateSpeechFileException(f'Failed to generate speech file ({filePaths=}) ({command=}) ({outputString=}) ({exception=})')

        return filePaths.fullFilePath

    async def __killCommodoreSamProcess(self, commodoreSamProcess: Process | None):
        if commodoreSamProcess is None:
            self.__timber.log('CommodoreSamApiService', f'Went to kill the Commodore SAM process, but the process is None ({commodoreSamProcess=})')
            return
        elif not isinstance(commodoreSamProcess, Process):
            raise TypeError(f'process argument is malformed: \"{commodoreSamProcess}\"')
        elif commodoreSamProcess.returncode is not None:
            self.__timber.log('CommodoreSamApiService', f'Went to kill a Commodore SAM process, but the process has a return code ({commodoreSamProcess=}) ({commodoreSamProcess.returncode=})')
            return

        self.__timber.log('CommodoreSamApiService', f'Killing Commodore SAM process ({commodoreSamProcess=}) ({commodoreSamProcess.returncode=})...')
        parent = psutil.Process(commodoreSamProcess.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__timber.log('CommodoreSamApiService', f'Finished killing Commodore SAM process ({commodoreSamProcess=}) ({commodoreSamProcess.returncode=}) ({childCount=})')
