import queue
import traceback
from queue import SimpleQueue
from typing import Final

from .chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..listeners.useChatterItemEventListener import UseChatterItemEventListener
from ..models.events.useChatterItemEvent import UseChatterItemEvent
from ..models.useChatterItemAction import UseChatterItemAction
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface


class ChatterInventoryItemUseMachine(ChatterInventoryItemUseMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[UseChatterItemAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[UseChatterItemEvent]] = SimpleQueue()
        self.__eventListener: UseChatterItemEventListener | None = None

    def setEventListener(self, listener: UseChatterItemEventListener | None):
        if listener is not None and not isinstance(listener, UseChatterItemEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__eventListener = listener

    def start(self):
        if self.__isStarted:
            self.__timber.log('ChatterInventoryItemUseMachine', 'Not starting ChatterInventoryItemUseMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('ChatterInventoryItemUseMachine', 'Starting ChatterInventoryItemUseMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startActionLoop(self):
        # TODO
        pass

    async def __startEventLoop(self):
        # TODO
        pass

    def submitAction(self, action: UseChatterItemAction):
        if not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitEvent(self, event: UseChatterItemEvent):
        if not isinstance(event, UseChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
