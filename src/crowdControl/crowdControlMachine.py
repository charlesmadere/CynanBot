import asyncio
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Final

from .actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from .actions.crowdControlAction import CrowdControlAction
from .actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from .crowdControlActionHandleResult import CrowdControlActionHandleResult
from .crowdControlActionHandler import CrowdControlActionHandler
from .crowdControlMachineInterface import CrowdControlMachineInterface
from .exceptions import ActionHandlerProcessCantBeConnectedToException, ActionHandlerProcessNotFoundException
from .idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from .message.crowdControlMessage import CrowdControlMessage
from .message.crowdControlMessageListener import CrowdControlMessageListener
from .settings.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.soundAlert import SoundAlert
from ..timber.timberInterface import TimberInterface


class CrowdControlMachine(CrowdControlMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__crowdControlIdGenerator: Final[CrowdControlIdGeneratorInterface] = crowdControlIdGenerator
        self.__crowdControlSettingsRepository: Final[CrowdControlSettingsRepositoryInterface] = crowdControlSettingsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isPaused: bool = False
        self.__isStarted: bool = False
        self.__actionHandler: CrowdControlActionHandler | None = None
        self.__messageListener: CrowdControlMessageListener | None = None
        self.__actionQueue: Final[SimpleQueue[CrowdControlAction]] = SimpleQueue()
        self.__messageQueue: Final[SimpleQueue[CrowdControlMessage]] = SimpleQueue()

    async def __handleAction(
        self,
        action: CrowdControlAction,
        actionHandler: CrowdControlActionHandler,
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(actionHandler, CrowdControlActionHandler):
            raise TypeError(f'actionHandler argument is malformed: \"{actionHandler}\"')

        action.incrementHandleAttempts()
        if action.handleAttempts >= await self.__crowdControlSettingsRepository.getMaxHandleAttempts():
            self.__timber.log('CrowdControlMachine', f'Abandoning action due to too many handle attempts ({action=})')
            return CrowdControlActionHandleResult.ABANDON

        now = datetime.now(self.__timeZoneRepository.getDefault())
        if now > action.dateTime + timedelta(seconds = await self.__crowdControlSettingsRepository.getSecondsToLive()):
            self.__timber.log('CrowdControlMachine', f'Abandoning action due to age exceeding time to live ({action=})')
            return CrowdControlActionHandleResult.ABANDON

        if not await self.__crowdControlSettingsRepository.isEnabled():
            self.__timber.log('CrowdControlMachine', f'Retrying action due to Crowd Control being disabled ({action=})')
            return CrowdControlActionHandleResult.RETRY

        if await self.__crowdControlSettingsRepository.areSoundsEnabled():
            self.__backgroundTaskHelper.createTask(self.__playSoundAlert(action))

        handleResult: CrowdControlActionHandleResult

        if isinstance(action, ButtonPressCrowdControlAction):
            handleResult = await self.__handleButtonPressAction(
                action = action,
                actionHandler = actionHandler,
            )
        elif isinstance(action, GameShuffleCrowdControlAction):
            handleResult = await self.__handleGameShuffleAction(
                action = action,
                actionHandler = actionHandler,
            )
        else:
            raise TypeError(f'Encountered unknown CrowdControlAction type: ({action=})')

        if handleResult is not CrowdControlActionHandleResult.OK:
            self.__timber.log('CrowdControlMachine', f'Failed to handle action ({action=}) ({handleResult=})')

        return handleResult

    async def __handleButtonPressAction(
        self,
        action: ButtonPressCrowdControlAction,
        actionHandler: CrowdControlActionHandler,
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, ButtonPressCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(actionHandler, CrowdControlActionHandler):
            raise TypeError(f'actionHandler argument is malformed: \"{actionHandler}\"')

        try:
            return await actionHandler.handleButtonPressAction(action)
        except ActionHandlerProcessCantBeConnectedToException as e:
            self.__timber.log('CrowdControlMachine', f'Unable to connect to action handler process when handling button press action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except ActionHandlerProcessNotFoundException as e:
            self.__timber.log('CrowdControlMachine', f'Unable to find action handler process when handling button press action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except PermissionError as e:
            self.__timber.log('CrowdControlMachine', f'Don\'t have permission to handle button press action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except Exception as e:
            self.__timber.log('CrowdControlMachine', f'Encountered unknown Exception when handling button press action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.RETRY

    async def __handleGameShuffleAction(
        self,
        action: GameShuffleCrowdControlAction,
        actionHandler: CrowdControlActionHandler,
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, GameShuffleCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(actionHandler, CrowdControlActionHandler):
            raise TypeError(f'actionHandler argument is malformed: \"{actionHandler}\"')

        try:
            return await actionHandler.handleGameShuffleAction(action)
        except ActionHandlerProcessCantBeConnectedToException as e:
            self.__timber.log('CrowdControlMachine', f'Unable to connect to action handler process when handling game shuffle action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except ActionHandlerProcessNotFoundException as e:
            self.__timber.log('CrowdControlMachine', f'Unable to find action handler process when handling game shuffle action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except PermissionError as e:
            self.__timber.log('CrowdControlMachine', f'Don\'t have permission to handle game shuffle action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON
        except Exception as e:
            self.__timber.log('CrowdControlMachine', f'Encountered unknown Exception when handling game shuffle action ({action=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.RETRY

    @property
    def isPaused(self) -> bool:
        return self.__isPaused

    def pause(self) -> bool:
        isAlreadyPaused = self.isPaused

        if not isAlreadyPaused:
            self.__isPaused = True

        # indicates to the caller that we were previously resumed, but are now paused
        return not isAlreadyPaused

    async def __playSoundAlert(self, action: CrowdControlAction):
        if not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__crowdControlSettingsRepository.areSoundsEnabled():
            return

        alert: SoundAlert | None = None

        if isinstance(action, ButtonPressCrowdControlAction):
            alert = SoundAlert.CLICK_NAVIGATION
        elif isinstance(action, GameShuffleCrowdControlAction):
            entryWithinGigaShuffle = action.entryWithinGigaShuffle
            startOfGigaShuffleSize = action.startOfGigaShuffleSize

            if not entryWithinGigaShuffle and startOfGigaShuffleSize is not None and startOfGigaShuffleSize >= 2:
                alert = SoundAlert.JACKPOT
        else:
            raise TypeError(f'Encountered unknown CrowdControlAction type: ({action=})')

        if alert is None:
            return

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        await soundPlayerManager.playSoundAlert(
            alert = alert,
            volume = await self.__crowdControlSettingsRepository.getMediaPlayerVolume(),
        )

    def resume(self) -> bool:
        isAlreadyResumed = not self.isPaused

        if not isAlreadyResumed:
            self.__isPaused = False

        # indicates to the caller that we were previously paused, but are now resumed
        return not isAlreadyResumed

    def setActionHandler(self, actionHandler: CrowdControlActionHandler | None):
        if actionHandler is not None and not isinstance(actionHandler, CrowdControlActionHandler):
            raise TypeError(f'actionHandler argument is malformed: \"{actionHandler}\"')

        self.__actionHandler = actionHandler

    def setMessageListener(self, messageListener: CrowdControlMessageListener | None):
        if messageListener is not None and not isinstance(messageListener, CrowdControlMessageListener):
            raise TypeError(f'messageListener argument is malformed: \"{messageListener}\"')

        self.__messageListener = messageListener

    def start(self):
        if self.__isStarted:
            self.__timber.log('CrowdControlMachine', 'Not starting CrowdControlMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CrowdControlMachine', 'Starting CrowdControlMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())
        self.__backgroundTaskHelper.createTask(self.__startMessageLoop())

    async def __startActionLoop(self):
        while True:
            actionHandler = self.__actionHandler

            if actionHandler is not None and not self.isPaused:
                action: CrowdControlAction | None = None

                try:
                    if not self.__actionQueue.empty():
                        action = self.__actionQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('CrowdControlMachine', f'Encountered queue.Empty when grabbing action (queue size: {self.__actionQueue.qsize()}) ({action=}): {e}', e, traceback.format_exc())

                if action is not None:
                    result = await self.__handleAction(
                        action = action,
                        actionHandler = actionHandler,
                    )

                    match result:
                        case CrowdControlActionHandleResult.OK:
                            await self.__submitMessage(action)

                        case CrowdControlActionHandleResult.RETRY:
                            self.submitAction(action)

                        case _:
                            # this case is intentionally ignored
                            pass

            actionLoopCooldownSeconds = await self.__crowdControlSettingsRepository.getActionLoopCooldownSeconds()
            await asyncio.sleep(actionLoopCooldownSeconds)

    async def __startMessageLoop(self):
        while True:
            messageListener = self.__messageListener

            if messageListener is not None:
                message: CrowdControlMessage | None = None

                try:
                    if not self.__messageQueue.empty():
                        message = self.__messageQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('CrowdControlMachine', f'Encountered queue.Empty when grabbing message (queue size: {self.__messageQueue.qsize()}) ({message=}): {e}', e, traceback.format_exc())

                if message is not None:
                    await messageListener.onNewCrowdControlMessage(message)

            messageCooldownSeconds = await self.__crowdControlSettingsRepository.getMessageCooldownSeconds()
            await asyncio.sleep(messageCooldownSeconds)

    def submitAction(self, action: CrowdControlAction):
        if not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('CrowdControlMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitMessage(self, action: CrowdControlAction):
        if not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not isinstance(action, GameShuffleCrowdControlAction) or action.startOfGigaShuffleSize is None or action.startOfGigaShuffleSize <= 1:
            # this is kind of stupid but oh well it's the best/simplest way to do this for now, as I'm only currently
            # intending to send a message to the chat if we're currently processing a giga shuffle
            return

        message = CrowdControlMessage(
            originatingAction = action,
            messageId = await self.__crowdControlIdGenerator.generateMessageId(),
        )

        try:
            self.__messageQueue.put_nowait(message)
        except queue.Full as e:
            self.__timber.log('CrowdControlMachine', f'Encountered queue.Full when submitting a new message ({message}) into the giga shuffle message queue (queue size: {self.__messageQueue.qsize()}): {e}', e, traceback.format_exc())
