import asyncio
import queue
import traceback
from queue import SimpleQueue

from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from .currentStreamAlert import CurrentStreamAlert
from .streamAlert import StreamAlert
from .streamAlertsManagerInterface import StreamAlertsManagerInterface
from .streamAlertsSettingsRepositoryInterface import \
    StreamAlertsSettingsRepositoryInterface
from .streamAlertState import StreamAlertState
from ..timber.timberInterface import TimberInterface
from ..tts.ttsManagerInterface import TtsManagerInterface


class StreamAlertsManager(StreamAlertsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerManager: SoundPlayerManagerInterface | None,
        streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsManager: TtsManagerInterface | None,
        queueSleepTimeSeconds: float = 0.2,
        queueTimeoutSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif soundPlayerManager is not None and not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(streamAlertsSettingsRepository, StreamAlertsSettingsRepositoryInterface):
            raise TypeError(f'streamAlertsSettingsRepository argument is malformed: \"{streamAlertsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise TypeError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 0.10 or queueSleepTimeSeconds > 8:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 3:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__soundPlayerManager: SoundPlayerManagerInterface | None = soundPlayerManager
        self.__streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface = streamAlertsSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsManager: TtsManagerInterface | None = ttsManager
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__currentAlert: CurrentStreamAlert | None = None
        self.__alertQueue: SimpleQueue[StreamAlert] = SimpleQueue()

    async def __processCurrentAlert(self) -> bool:
        currentAlert = self.__currentAlert

        if currentAlert is None:
            return False

        soundPlayerManager = self.__soundPlayerManager
        soundAlert = currentAlert.getSoundAlert()
        ttsManager = self.__ttsManager
        ttsEvent = currentAlert.getTtsEvent()

        if (currentAlert.getAlertState() is StreamAlertState.NOT_STARTED or currentAlert.getAlertState() is StreamAlertState.SOUND_STARTED) and soundAlert is not None and soundPlayerManager is not None:
            if await soundPlayerManager.isPlaying():
                return True
            elif currentAlert.getAlertState() is StreamAlertState.SOUND_STARTED:
                currentAlert.setAlertState(StreamAlertState.SOUND_FINISHED)
            elif await soundPlayerManager.playSoundAlert(soundAlert):
                currentAlert.setAlertState(StreamAlertState.SOUND_STARTED)
                return True
            else:
                currentAlert.setAlertState(StreamAlertState.SOUND_FINISHED)

        if (currentAlert.getAlertState() is StreamAlertState.NOT_STARTED or currentAlert.getAlertState() is StreamAlertState.TTS_STARTED or currentAlert.getAlertState() is StreamAlertState.SOUND_FINISHED) and ttsEvent is not None and ttsManager is not None:
            if await ttsManager.isPlaying():
                return True
            elif currentAlert.getAlertState() is StreamAlertState.TTS_STARTED:
                currentAlert.setAlertState(StreamAlertState.TTS_FINISHED)
            elif await ttsManager.playTtsEvent(ttsEvent):
                currentAlert.setAlertState(StreamAlertState.TTS_STARTED)
                return True
            else:
                currentAlert.setAlertState(StreamAlertState.TTS_FINISHED)

        self.__currentAlert = None
        return False

    def start(self):
        if self.__isStarted:
            self.__timber.log('StreamAlertsManager', 'Not starting StreamAlertsManager as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('StreamAlertsManager', 'Starting StreamAlertsManager...')
        self.__backgroundTaskHelper.createTask(self.__startAlertLoop())

    async def __startAlertLoop(self):
        while True:
            if await self.__processCurrentAlert():
                await asyncio.sleep(self.__queueSleepTimeSeconds)
                continue

            newAlert: StreamAlert | None = None

            if not self.__alertQueue.empty():
                try:
                    newAlert = self.__alertQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('StreamAlertsManager', f'Encountered queue.Empty when grabbing alert from queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())

            if newAlert is not None:
                self.__currentAlert = CurrentStreamAlert(newAlert)

            await asyncio.sleep(await self.__streamAlertsSettingsRepository.getAlertsDelayBetweenSeconds())

    def submitAlert(self, alert: StreamAlert):
        if not isinstance(alert, StreamAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        try:
            self.__alertQueue.put(alert, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('StreamAlertsManager', f'Encountered queue.Full when submitting a new alert ({alert}) into the alert queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())
