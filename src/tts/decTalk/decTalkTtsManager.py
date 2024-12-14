import asyncio
from asyncio import CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import ByteString

import aiofiles.ospath
import psutil

from .decTalkFileManagerInterface import DecTalkFileManagerInterface
from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ...decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class DecTalkTtsManager(DecTalkTtsManagerInterface):

    def __init__(
        self,
        decTalkFileManager: DecTalkFileManagerInterface,
        decTalkMessageCleaner: DecTalkMessageCleanerInterface,
        decTalkVoiceChooser: DecTalkVoiceChooserInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
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

        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__decTalkMessageCleaner: DecTalkMessageCleanerInterface = decTalkMessageCleaner
        self.__decTalkVoiceChooser: DecTalkVoiceChooserInterface = decTalkVoiceChooser
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False
        self.__decTalkProcess: Process | None = None

    async def __applyRandomVoice(self, command: str) -> str:
        updatedCommand = await self.__decTalkVoiceChooser.choose(command)

        if utils.isValidStr(updatedCommand):
            self.__timber.log('DecTalkManager', f'Applied random DecTalk voice')
            return updatedCommand
        else:
            return command

    async def __executeTts(self, command: str):
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()
        decTalkProcess: Process | None = None
        outputTuple: tuple[ByteString, ByteString] | None = None
        exception: BaseException | None = None

        try:
            decTalkProcess = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            self.__decTalkProcess = decTalkProcess

            outputTuple = await asyncio.wait_for(
                fut = decTalkProcess.communicate(),
                timeout = timeoutSeconds
            )
        except BaseException as e:
            exception = e

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killDecTalkProcess(decTalkProcess)

        decTalkProcess = None
        self.__decTalkProcess = None
        outputString: str | None = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__isLoadingOrPlaying = False
        self.__timber.log('DecTalkManager', f'Ran DecTalk system command ({command=}) ({outputString=}) ({exception=})')

    async def __killDecTalkProcess(self, decTalkProcess: Process | None):
        if decTalkProcess is None:
            self.__isLoadingOrPlaying = False
            self.__timber.log('DecTalkManager', f'Went to kill the DecTalk process, but the process is None ({decTalkProcess=})')
            return
        elif not isinstance(decTalkProcess, Process):
            raise TypeError(f'process argument is malformed: \"{decTalkProcess}\"')
        elif decTalkProcess.returncode is not None:
            self.__isLoadingOrPlaying = False
            self.__timber.log('DecTalkManager', f'Went to kill a DecTalk process, but the process has a return code ({decTalkProcess=}) ({decTalkProcess.returncode=})')
            return

        self.__timber.log('DecTalkManager', f'Killing DecTalk process ({decTalkProcess=})...')
        parent = psutil.Process(decTalkProcess.pid)
        childCount = 0

        for child in parent.children(recursive = True):
            child.terminate()
            childCount += 1

        parent.terminate()
        self.__isLoadingOrPlaying = False
        self.__timber.log('DecTalkManager', f'Finished killing DecTalk process ({decTalkProcess=}) ({childCount=})')

    @property
    def isLoadingOrPlaying(self) -> bool:
        return self.__isLoadingOrPlaying or self.__decTalkProcess is not None

    async def playTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return
        elif self.isLoadingOrPlaying:
            self.__timber.log('DecTalkManager', f'There is already an ongoing DecTalk event!')
            return

        self.__isLoadingOrPlaying = True
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('DecTalkManager', f'Failed to write TTS message in \"{event.twitchChannel}\" to temporary file ({event=}) ({fileName=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('DecTalkManager', f'Executing TTS message in \"{event.twitchChannel}\"...')
        pathToDecTalk = await self.__ttsSettingsRepository.requireDecTalkPath()
        await self.__executeTts(f'{pathToDecTalk} -pre \"[:phone on]\" < \"{fileName}\"')

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

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__killDecTalkProcess(self.__decTalkProcess)

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
