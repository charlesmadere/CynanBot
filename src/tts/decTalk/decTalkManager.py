import asyncio
from asyncio import CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import Any, ByteString

import aiofiles.ospath
import psutil

from .decTalkFileManagerInterface import DecTalkFileManagerInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ...decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class DecTalkManager(TtsManagerInterface):

    def __init__(
        self,
        decTalkFileManager: DecTalkFileManagerInterface,
        decTalkMessageCleaner: DecTalkMessageCleanerInterface,
        decTalkVoiceChooser: DecTalkVoiceChooserInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
    ):
        if not isinstance(decTalkFileManager, DecTalkFileManagerInterface):
            raise TypeError(f'decTalkFileManager argument is malformed: \"{decTalkFileManager}\"')
        elif not isinstance(decTalkMessageCleaner, DecTalkMessageCleanerInterface):
            raise TypeError(f'decTalkMessageCleaner argument is malformed: \"{decTalkMessageCleaner}\"')
        elif not isinstance(decTalkVoiceChooser, DecTalkVoiceChooserInterface):
            raise TypeError(f'decTalkVoiceChooser argument is malformed: \"{decTalkVoiceChooser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__decTalkMessageCleaner: DecTalkMessageCleanerInterface = decTalkMessageCleaner
        self.__decTalkVoiceChooser: DecTalkVoiceChooserInterface = decTalkVoiceChooser
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

        self.__isLoading: bool = False
        self.__isPlaying: bool = False

    async def __applyRandomVoice(self, command: str) -> str:
        updatedCommand = await self.__decTalkVoiceChooser.choose(command)

        if utils.isValidStr(updatedCommand):
            self.__timber.log('DecTalkManager', f'Applied random DecTalk voice')
            return updatedCommand
        else:
            return command

    async def __executeDecTalkCommand(self, command: str):
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')

        if await self.isPlaying():
            self.__timber.log('DecTalkManager', f'There is already an ongoing Dec Talk event!')
            return

        self.__isPlaying = True
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        process: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        try:
            process = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            outputTuple = await asyncio.wait_for(
                fut = process.communicate(),
                timeout = timeoutSeconds
            )
        except BaseException as e:
            exception = e

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killDecTalkProcess(process)

        process = None
        outputString: str | None = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('DecTalkManager', f'Ran Dec Talk system command ({command}) ({outputString=}) ({exception=})')
        self.__isPlaying = False

    async def __killDecTalkProcess(self, process: Process | None):
        if process is None:
            self.__timber.log('DecTalkManager', f'Went to kill the Dec Talk process, but the process is None: \"{process}\"')
            return
        elif not isinstance(process, Process):
            raise TypeError(f'process argument is malformed: \"{process}\"')
        elif process.returncode is not None:
            self.__timber.log('DecTalkManager', f'Went to kill the Dec Talk process, but the process (\"{process}\") has a return code: \"{process.returncode}\"')
            return

        self.__timber.log('DecTalkManager', f'Killing Dec Talk process \"{process}\"...')
        parent = psutil.Process(process.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__timber.log('DecTalkManager', f'Finished killing process \"{process}\" ({childCount=})')

    async def isPlaying(self) -> bool:
        return self.__isLoading or self.__isPlaying

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('DecTalkManager', f'There is already an ongoing Dec Talk event!')
            return False

        self.__isLoading = True
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('DecTalkManager', f'Failed to write TTS message in \"{event.twitchChannel}\" to temporary file ({event=}) ({fileName=})')
            self.__isLoading = False
            return False

        self.__timber.log('DecTalkManager', f'Executing TTS message in \"{event.twitchChannel}\"...')
        pathToDecTalk = utils.cleanPath(await self.__ttsSettingsRepository.requireDecTalkPath())
        self.__isLoading = False

        await self.__executeDecTalkCommand(f'{pathToDecTalk} -pre \"[:phone on]\" < \"{fileName}\"')
        await self.__ttsTempFileHelper.registerTempFile(fileName)

        return True

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        message = await self.__decTalkMessageCleaner.clean(event.message)
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        fullMessage: str

        if utils.isValidStr(message) and utils.isValidStr(donationPrefix):
            fullMessage = f'{donationPrefix} {message}'
        elif utils.isValidStr(message):
            fullMessage = message
        elif utils.isValidStr(donationPrefix):
            fullMessage = donationPrefix
        else:
            return None

        message = await self.__applyRandomVoice(fullMessage)
        return await self.__decTalkFileManager.writeCommandToNewFile(message)

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isLoading': self.__isLoading,
            'isPlaying': self.__isPlaying
        }
