import asyncio
import os
import re
import uuid
from asyncio import AbstractEventLoop, CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import ByteString, Pattern

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
from ...tts.ttsProvider import TtsProvider


class CommodoreSamApiService(CommodoreSamApiServiceInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
        fileExtension: str = 'wav'
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

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface = commodoreSamSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsDirectoryProvider: TtsDirectoryProviderInterface = ttsDirectoryProvider
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        if await aiofiles.ospath.exists(
            path = filePath,
            loop = self.__eventLoop
        ):
            return

        await aiofiles.os.makedirs(
            name = filePath,
            loop = self.__eventLoop
        )

        self.__timber.log('CommodoreSamApiService', f'Created new directories ({filePath=})')

    async def __generateFileName(self) -> str:
        fileName = self.__fileNameRegEx.sub('', str(uuid.uuid4())).casefold()
        return f'{fileName}.{self.__fileExtension}'

    async def generateSpeechFile(self, text: str) -> str:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        self.__timber.log('CommodoreSamApiService', f'Generating speech... ({text=})')

        pathToCommodoreSam = await self.__commodoreSamSettingsRepository.requireCommodoreSamExecutablePath()

        if not await aiofiles.ospath.exists(
            path = pathToCommodoreSam,
            loop = self.__eventLoop
        ):
            raise CommodoreSamExecutableIsMissingException(f'Couldn\'t find Commodore SAM executable ({pathToCommodoreSam=})')

        filePath = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(TtsProvider.COMMODORE_SAM)
        await self.__createDirectories(filePath)

        fileName = await self.__generateFileName()
        fullFilePath = os.path.normpath(f'{filePath}/{fileName}')

        commodoreSamProcess: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        command = f'{os.path.normpath(pathToCommodoreSam)} -wav \"{fullFilePath}\" {text}'

        try:
            commodoreSamProcess = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            outputTuple = await asyncio.wait_for(
                fut = commodoreSamProcess.communicate(),
                timeout = 3
            )
        except BaseException as e:
            exception = e

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killCommodoreSamProcess(commodoreSamProcess)

        outputString: str | None = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('CommodoreSamApiService', f'Ran Commodore SAM system command ({command=}) ({outputString=}) ({exception=})')

        if not await aiofiles.ospath.exists(
            path = fullFilePath,
            loop = self.__eventLoop
        ):
            raise CommodoreSamFailedToGenerateSpeechFileException(f'Failed to generate speech file ({pathToCommodoreSam=}) ({fileName=}) ({filePath=}) ({command=}) ({outputString=}) ({exception=})')

        return fullFilePath

    async def __killCommodoreSamProcess(self, commodoreSamProcess: Process | None):
        if commodoreSamProcess is None:
            self.__timber.log('CommodoreSamApiService', f'Went to kill the Commodore SAM process, but the process is None ({commodoreSamProcess=})')
            return
        elif not isinstance(commodoreSamProcess, Process):
            raise TypeError(f'process argument is malformed: \"{commodoreSamProcess}\"')
        elif commodoreSamProcess.returncode is not None:
            self.__timber.log('CommodoreSamApiService', f'Went to kill a Commodore SAM process, but the process has a return code ({commodoreSamProcess=}) ({commodoreSamProcess.returncode=})')
            return

        self.__timber.log('CommodoreSamApiService', f'Killing Commodore SAM process ({commodoreSamProcess=})...')
        parent = psutil.Process(commodoreSamProcess.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__timber.log('CommodoreSamApiService', f'Finished killing Commodore SAM process ({commodoreSamProcess=}) ({childCount=})')
