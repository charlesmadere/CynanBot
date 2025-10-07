import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from .currentStreamAlert import CurrentStreamAlert
from .streamAlert import StreamAlert
from .streamAlertState import StreamAlertState
from .streamAlertsManagerInterface import StreamAlertsManagerInterface
from .streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..tts.models.ttsProvider import TtsProvider
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface


class StreamAlertsManager(StreamAlertsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface,
        timber: TimberInterface,
        queueSleepTimeSeconds: float = 0.25,
        queueTimeoutSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(streamAlertsSettingsRepository, StreamAlertsSettingsRepositoryInterface):
            raise TypeError(f'streamAlertsSettingsRepository argument is malformed: \"{streamAlertsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 0.10 or queueSleepTimeSeconds > 8:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 3:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__streamAlertsSettingsRepository: Final[StreamAlertsSettingsRepositoryInterface] = streamAlertsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__queueSleepTimeSeconds: Final[float] = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[float] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__currentAlert: CurrentStreamAlert | None = None
        self.__alertQueue: Final[SimpleQueue[StreamAlert]] = SimpleQueue()

    async def __createCurrentAlert(self, alert: StreamAlert) -> CurrentStreamAlert:
        compositeTtsManager: CompositeTtsManagerInterface
        soundPlayerManager: SoundPlayerManagerInterface

        if alert.ttsEvent is not None and alert.ttsEvent.provider is TtsProvider.SHOTGUN_TTS:
            compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
                useSharedSoundPlayerManager = False,
            )

            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        else:
            compositeTtsManager = self.__compositeTtsManagerProvider.getSharedInstance()
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()

        return CurrentStreamAlert(
            compositeTtsManager = compositeTtsManager,
            soundPlayerManager = soundPlayerManager,
            streamAlert = alert,
        )

    async def __processCurrentAlert(self) -> bool:
        currentAlert = self.__currentAlert

        if currentAlert is None:
            return False

        soundAlert = currentAlert.soundAlert
        soundPlayerManager = currentAlert.soundPlayerManager

        ttsEvent = currentAlert.ttsEvent
        compositeTtsManager = currentAlert.compositeTtsManager

        if (currentAlert.alertState is StreamAlertState.NOT_STARTED or currentAlert.alertState is StreamAlertState.SOUND_STARTED) and soundAlert is not None:
            if soundPlayerManager.isLoadingOrPlaying:
                return True
            elif currentAlert.alertState is StreamAlertState.SOUND_STARTED:
                currentAlert.setAlertState(StreamAlertState.SOUND_FINISHED)
            elif await soundPlayerManager.playSoundAlert(soundAlert):
                currentAlert.setAlertState(StreamAlertState.SOUND_STARTED)
                return True
            else:
                currentAlert.setAlertState(StreamAlertState.SOUND_FINISHED)

        if (currentAlert.alertState is StreamAlertState.NOT_STARTED or currentAlert.alertState is StreamAlertState.TTS_STARTED or currentAlert.alertState is StreamAlertState.SOUND_FINISHED) and ttsEvent is not None:
            if compositeTtsManager.isLoadingOrPlaying:
                return True
            elif currentAlert.alertState is StreamAlertState.TTS_STARTED:
                currentAlert.setAlertState(StreamAlertState.TTS_FINISHED)
            elif await compositeTtsManager.playTtsEvent(ttsEvent):
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
            try:
                if await self.__processCurrentAlert():
                    await asyncio.sleep(self.__queueSleepTimeSeconds)
                    continue
            except Exception as e:
                self.__timber.log('StreamAlertsManager', f'Encountered an error when processing current alert ({self.__currentAlert=})', e, traceback.format_exc())
                self.__currentAlert = None
                await asyncio.sleep(self.__queueSleepTimeSeconds)
                continue

            newAlert: StreamAlert | None = None

            if not self.__alertQueue.empty():
                try:
                    newAlert = self.__alertQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('StreamAlertsManager', f'Encountered queue.Empty when grabbing alert from queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())

            if newAlert is not None:
                self.__currentAlert = await self.__createCurrentAlert(newAlert)

            alertsDelayBetweenSeconds = await self.__streamAlertsSettingsRepository.getAlertsDelayBetweenSeconds()
            await asyncio.sleep(alertsDelayBetweenSeconds)

    def submitAlert(self, alert: StreamAlert):
        if not isinstance(alert, StreamAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        try:
            self.__alertQueue.put(alert, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('StreamAlertsManager', f'Encountered queue.Full when submitting a new alert ({alert}) into the alert queue (queue size: {self.__alertQueue.qsize()}): {e}', e, traceback.format_exc())
