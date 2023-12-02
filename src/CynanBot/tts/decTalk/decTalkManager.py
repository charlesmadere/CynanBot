import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
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
        backgroundTaskHelper: BackgroundTaskHelper,
        decTalkCommandBuilder: DecTalkCommandBuilder,
        decTalkFileManager: DecTalkFileManagerInterface,
        soundPlayerHelper: Optional[SoundPlayerHelperInterface],
        systemCommandHelper: SystemCommandHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        queueSleepTimeSeconds: float = 3,
        queueTimeoutSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(decTalkCommandBuilder, DecTalkCommandBuilder):
            raise ValueError(f'decTalkCommandBuilder argument is malformed: \"{decTalkCommandBuilder}\"')
        elif not isinstance(decTalkFileManager, DecTalkFileManagerInterface):
            raise ValueError(f'decTalkFileManager argument is malformed: \"{decTalkFileManager}\"')
        elif soundPlayerHelper is not None and not isinstance(soundPlayerHelper, SoundPlayerHelperInterface):
            raise ValueError(f'soundPlayerHelper argument is malformed: \"{soundPlayerHelper}\"')
        elif not isinstance(systemCommandHelper, SystemCommandHelperInterface):
            raise ValueError(f'systemCommandHelper argument is malformed: \"{systemCommandHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise ValueError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise ValueError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 10:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 3:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__soundPlayerHelper: Optional[SoundPlayerHelperInterface] = soundPlayerHelper
        self.__systemCommandHelper: SystemCommandHelperInterface = systemCommandHelper
        self.__timber: TimberInterface = timber
        self.__decTalkCommandBuilder: TtsCommandBuilderInterface = decTalkCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__eventQueue: SimpleQueue[TtsEvent] = SimpleQueue()

    async def __processTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isTtsEnabled():
            return

        command = await self.__decTalkCommandBuilder.buildAndCleanEvent(event)

        if not utils.isValidStr(command):
            self.__timber.log('DecTalkManager', f'Failed to parse TTS message in \"{event.getTwitchChannel()}\" into a valid command: \"{event}\"')
            return

        fileName = await self.__decTalkFileManager.writeCommandToNewFile(command)

        if not utils.isValidStr(fileName):
            self.__timber.log('DecTalkManager', f'Failed to write TTS message in \"{event.getTwitchChannel()}\" to temporary file ({command=})')
            return

        self.__timber.log('DecTalkManager', f'Executing TTS message in \"{event.getTwitchChannel()}\"...')
        pathToDecTalk = utils.cleanPath(await self.__ttsSettingsRepository.requireDecTalkPath())

        await self.__systemCommandHelper.executeCommand(
            command = f'{pathToDecTalk} -pre \"[:phone on]\" < \"{fileName}\"',
            timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()
        )

        await self.__decTalkFileManager.deleteFile(fileName)

    def start(self):
        if self.__isStarted:
            self.__timber.log('DecTalkManager', 'Not starting DecTalkManager as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('DecTalkManager', 'Starting DecTalkManager...')

        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startEventLoop(self):
        while True:
            event: Optional[TtsEvent] = None

            if not self.__eventQueue.empty():
                try:
                    event = self.__eventQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('DecTalkManager', f'Encountered queue.Empty when grabbing event from queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

            if event is None:
                await asyncio.sleep(self.__queueSleepTimeSeconds)
                continue

            try:
                await self.__processTtsEvent(event)
            except Exception as e:
                self.__timber.log('DecTalkManager', f'Encountered unexpected exception when processing TTS event (event: {event}) (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

            await asyncio.sleep(await self.__ttsSettingsRepository.getTtsDelayBetweenSeconds())

    def submitTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('DecTalkManager', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
