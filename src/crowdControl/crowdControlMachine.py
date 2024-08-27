import asyncio
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue

from .crowdControlInput import CrowdControlInput
from .crowdControlInputHandler import CrowdControlInputHandler
from .crowdControlInputResult import CrowdControlInputResult
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
        self.__inputHandler: CrowdControlInputHandler | None = None
        self.__inputQueue: SimpleQueue[CrowdControlInput] = SimpleQueue()

    async def __handleInput(
        self,
        input: CrowdControlInput,
        inputHandler: CrowdControlInputHandler
    ) -> CrowdControlInputResult:
        if not isinstance(input, CrowdControlInput):
            raise TypeError(f'input argument is malformed: \"{input}\"')
        elif not isinstance(inputHandler, CrowdControlInputHandler):
            raise TypeError(f'inputHandler argument is malformed: \"{inputHandler}\"')

        input.incrementHandleAttempts()
        if input.handleAttempts >= await self.__crowdControlSettingsRepository.getMaxHandleAttempts():
            self.__timber.log('CrowdControlMachine', f'Abandoning input due to too many handle attempts ({input=})')
            return CrowdControlInputResult.ABANDON

        now = datetime.now(self.__timeZoneRepository.getDefault())
        if now > input.dateTime + timedelta(seconds = await self.__crowdControlSettingsRepository.getSecondsToLive()):
            self.__timber.log('CrowdControlMachine', f'Abandoning input due to age exceeding time to live ({input=})')
            return CrowdControlInputResult.ABANDON

        handled: bool

        try:
            handled = await inputHandler.handleInput(input)
        except Exception as e:
            self.__timber.log('CrowdControlMachine', f'Encountered unknown Exception when handling input ({input=}): {e}', e, traceback.format_exc())
            handled = False

        if handled:
            return CrowdControlInputResult.OK

        self.__timber.log('CrowdControlMachine', f'Failed to handle input ({input=}), will potentially retry')
        return CrowdControlInputResult.RETRY

    def setInputHandler(self, inputHandler: CrowdControlInputHandler | None):
        if inputHandler is not None and not isinstance(inputHandler, CrowdControlInputHandler):
            raise TypeError(f'inputHandler argument is malformed: \"{inputHandler}\"')

        self.__inputHandler = inputHandler

    def start(self):
        if self.__isStarted:
            self.__timber.log('CrowdControlMachine', 'Not starting CrowdControlMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CrowdControlMachine', 'Starting CrowdControlMachine...')
        self.__backgroundTaskHelper.createTask(self.__startInputLoop())

    async def __startInputLoop(self):
        while True:
            inputHandler = self.__inputHandler

            if inputHandler is not None:
                input: CrowdControlInput | None = None

                try:
                    if not self.__inputQueue.empty():
                        input = self.__inputQueue.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('CrowdControlMachine', f'Encountered queue.Empty when grabbing input (queue size: {self.__inputQueue.qsize()}) ({input=}): {e}', e, traceback.format_exc())

                if input is not None:
                    result = await self.__handleInput(
                        input = input,
                        inputHandler = inputHandler
                    )

                    if result is CrowdControlInputResult.RETRY:
                        self.submitInput(input)

            inputCooldownSeconds = await self.__crowdControlSettingsRepository.getInputCooldownSeconds()
            await asyncio.sleep(inputCooldownSeconds)

    def submitInput(self, input: CrowdControlInput):
        if not isinstance(input, CrowdControlInput):
            raise TypeError(f'input argument is malformed: \"{input}\"')

        try:
            self.__inputQueue.put(input, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('CrowdControlMachine', f'Encountered queue.Full when submitting a new input ({input}) into the input queue (queue size: {self.__inputQueue.qsize()}): {e}', e, traceback.format_exc())
