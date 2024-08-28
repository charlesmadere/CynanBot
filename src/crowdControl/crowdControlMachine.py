import asyncio
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue

from .actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from .actions.crowdControlAction import CrowdControlAction
from .actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from .crowdControlActionHandleResult import CrowdControlActionHandleResult
from .crowdControlActionHandler import CrowdControlActionHandler
from .crowdControlMachineInterface import CrowdControlMachineInterface
from .crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class CrowdControlMachine(CrowdControlMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        queueTimeoutSeconds: int = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface = crowdControlSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionHandler: CrowdControlActionHandler | None = None
        self.__actionQueue: SimpleQueue[CrowdControlAction] = SimpleQueue()

    async def __handleAction(
        self,
        action: CrowdControlAction,
        actionHandler: CrowdControlActionHandler
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

        handled = False

        if isinstance(action, ButtonPressCrowdControlAction):
            try:
                handled = await actionHandler.handleButtonPressAction(action)
            except Exception as e:
                self.__timber.log('CrowdControlMachine', f'Encountered unknown Exception when handling button press action ({action=}): {e}', e, traceback.format_exc())
        elif isinstance(action, GameShuffleCrowdControlAction):
            try:
                handled = await actionHandler.handleGameShuffleAction(action)
            except Exception as e:
                self.__timber.log('CrowdControlMachine', f'Encountered unknown Exception when handling game shuffle action ({action=}): {e}', e, traceback.format_exc())
        else:
            raise TypeError(f'Encountered unknown CrowdControlAction type: ({action=})')

        if handled:
            return CrowdControlActionHandleResult.OK

        self.__timber.log('CrowdControlMachine', f'Failed to handle action ({action=}), will potentially retry')
        return CrowdControlActionHandleResult.RETRY

    def setActionHandler(self, actionHandler: CrowdControlActionHandler | None):
        if actionHandler is not None and not isinstance(actionHandler, CrowdControlActionHandler):
            raise TypeError(f'actionHandler argument is malformed: \"{actionHandler}\"')

        self.__actionHandler = actionHandler

    def start(self):
        if self.__isStarted:
            self.__timber.log('CrowdControlMachine', 'Not starting CrowdControlMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CrowdControlMachine', 'Starting CrowdControlMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())

    async def __startActionLoop(self):
        while True:
            actionHandler = self.__actionHandler

            if actionHandler is not None:
                action: CrowdControlAction | None = None

                try:
                    if not self.__actionQueue.empty():
                        action = self.__actionQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('CrowdControlMachine', f'Encountered queue.Empty when grabbing action (queue size: {self.__actionQueue.qsize()}) ({action=}): {e}', e, traceback.format_exc())

                if action is not None:
                    result = await self.__handleAction(
                        action = action,
                        actionHandler = actionHandler
                    )

                    if result is CrowdControlActionHandleResult.RETRY:
                        self.submitAction(action)

            actionCooldownSeconds = await self.__crowdControlSettingsRepository.getActionCooldownSeconds()
            await asyncio.sleep(actionCooldownSeconds)

    def submitAction(self, action: CrowdControlAction):
        if not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('CrowdControlMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())
