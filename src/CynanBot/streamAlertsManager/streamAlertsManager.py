import asyncio
import queue
import traceback
from CynanBot.soundPlayerHelper.soundReferenceInterface import SoundReferenceInterface
from queue import SimpleQueue
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.streamAlertsManager.streamAlertsSettingsRepositoryInterface import \
    StreamAlertsSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface


class StreamAlertsManager(StreamAlertsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        soundPlayerHelper: Optional[SoundPlayerHelperInterface],
        streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface],
        queueSleepTimeSeconds: float = 3,
        queueTimeoutSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif soundPlayerHelper is not None and not isinstance(soundPlayerHelper, SoundPlayerHelperInterface):
            raise TypeError(f'soundPlayerHelper argument is malformed: \"{soundPlayerHelper}\"')
        elif not isinstance(streamAlertsSettingsRepository, StreamAlertsSettingsRepositoryInterface):
            raise TypeError(f'streamAlertsSettingsRepository argument is malformed: \"{streamAlertsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise TypeError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 10:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 3:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__soundPlayerHelper: Optional[SoundPlayerHelperInterface] = soundPlayerHelper
        self.__streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface = streamAlertsSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__alertQueue: SimpleQueue[StreamAlert] = SimpleQueue()

    async def __processAlert(self, alert: StreamAlert):
        if not isinstance(alert, StreamAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        ttsEvent = alert.getTtsEvent()

        if ttsEvent is not None and self.__ttsManager is not None:
            await self.__ttsManager.processTtsEvent(ttsEvent)

        soundAlert = alert.getSoundAlert()
        soundReference: Optional[SoundReferenceInterface] = None

        if soundAlert is not None and self.__soundPlayerHelper is not None:
            soundReference = await self.__soundPlayerHelper.loadSoundAlert(soundAlert)

        # TODO
        pass

    def start(self):
        if self.__isStarted:
            self.__timber.log('StreamAlertsManager', 'Not starting StreamAlertsManager as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('StreamAlertsManager', 'Starting StreamAlertsManager...')

        self.__backgroundTaskHelper.createTask(self.__startAlertLoop())

    async def __startAlertLoop(self):
        while True:
            alert: Optional[StreamAlert] = None

            if not self.__alertQueue.empty():
                try:
                    alert = self.__alertQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('StreamAlertsManager', f'Encountered queue.Empty when grabbing alert from queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())

            if alert is None:
                await asyncio.sleep(self.__queueSleepTimeSeconds)
                continue

            try:
                await self.__processAlert(alert)
            except Exception as e:
                self.__timber.log('StreamAlertsManager', f'Encountered unexpected exception when processing alert (alert: {alert}) (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())

            await asyncio.sleep(await self.__streamAlertsSettingsRepository.getAlertsDelayBetweenSeconds())

    def submitAlert(self, alert: StreamAlert):
        if not isinstance(alert, StreamAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        try:
            self.__alertQueue.put(alert, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('StreamAlertsManager', f'Encountered queue.Full when submitting a new alert ({alert}) into the alert queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())
