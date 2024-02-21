import asyncio
from asyncio import CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import Any, ByteString, Dict, Optional, Tuple

import psutil

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkCommandBuilder import DecTalkCommandBuilder
from CynanBot.tts.decTalk.decTalkFileManagerInterface import \
    DecTalkFileManagerInterface
from CynanBot.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class DecTalkManager(TtsManagerInterface):

    def __init__(
        self,
        decTalkCommandBuilder: DecTalkCommandBuilder,
        decTalkFileManager: DecTalkFileManagerInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        assert isinstance(decTalkCommandBuilder, DecTalkCommandBuilder), f"malformed {decTalkCommandBuilder=}"
        assert isinstance(decTalkFileManager, DecTalkFileManagerInterface), f"malformed {decTalkFileManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface), f"malformed {ttsSettingsRepository=}"

        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__timber: TimberInterface = timber
        self.__decTalkCommandBuilder: TtsCommandBuilderInterface = decTalkCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isPlaying: bool = False

    async def __executeDecTalkCommand(self, command: str):
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')

        if await self.isPlaying():
            self.__timber.log('DecTalkManager', f'There is already an ongoing Dec Talk event!')
            return

        self.__isPlaying = True
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        process: Optional[Process] = None
        outputTuple: Optional[Tuple[ByteString, ByteString]] = None
        exception: Optional[BaseException] = None

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
        outputString: Optional[str] = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('DecTalkManager', f'Ran Dec Talk system command ({command}) ({outputString=}) ({exception=})')
        self.__isPlaying = False

    async def __killDecTalkProcess(self, process: Optional[Process]):
        if process is None:
            self.__timber.log('DecTalkManager', f'Went to kill the Dec Talk process, but the process is None: \"{process}\"')
            return
        elassert isinstance(process, Process), f"malformed {process=}"
        if process.returncode is not None:
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
        return self.__isPlaying

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        assert isinstance(event, TtsEvent), f"malformed {event=}"

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('DecTalkManager', f'There is already an ongoing Dec Talk event!')
            return False

        command = await self.__decTalkCommandBuilder.buildAndCleanEvent(event)

        if not utils.isValidStr(command):
            self.__timber.log('DecTalkManager', f'Failed to parse TTS message in \"{event.getTwitchChannel()}\" into a valid command: \"{event}\"')
            return False

        fileName = await self.__decTalkFileManager.writeCommandToNewFile(command)

        if not utils.isValidStr(fileName):
            self.__timber.log('DecTalkManager', f'Failed to write TTS message in \"{event.getTwitchChannel()}\" to temporary file ({command=})')
            return False

        self.__timber.log('DecTalkManager', f'Executing TTS message in \"{event.getTwitchChannel()}\"...')
        pathToDecTalk = utils.cleanPath(await self.__ttsSettingsRepository.requireDecTalkPath())
        await self.__executeDecTalkCommand(f'{pathToDecTalk} -pre \"[:phone on]\" < \"{fileName}\"')
        await self.__decTalkFileManager.deleteFile(fileName)

        return True

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'isPlaying': self.__isPlaying
        }
