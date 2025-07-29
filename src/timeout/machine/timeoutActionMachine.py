import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..exceptions import UnknownTimeoutActionTypeException
from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.absTimeoutAction import AbsTimeoutAction
from ..models.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.bananaTimeoutAction import BananaTimeoutAction
from ..models.basicTimeoutAction import BasicTimeoutAction
from ..models.grenadeTimeoutAction import GrenadeTimeoutAction
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface


class TimeoutActionMachine(TimeoutActionMachineInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        sleepTimeSeconds: float = 2,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[AbsTimeoutAction]] = SimpleQueue()
        self.__listener: TimeoutEventListener | None = None

    async def __handleAirStrikeTimeoutAction(self, action: AirStrikeTimeoutAction):
        if not isinstance(action, AirStrikeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        pass

    async def __handleBananaTimeoutAction(self, action: BananaTimeoutAction):
        if not isinstance(action, BananaTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        pass

    async def __handleBasicTimeoutAction(self, action: BasicTimeoutAction):
        if not isinstance(action, BasicTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        pass

    async def __handleGrenadeTimeoutAction(self, action: GrenadeTimeoutAction):
        if not isinstance(action, GrenadeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        pass

    async def __handleTimeoutAction(self, action: AbsTimeoutAction):
        if not isinstance(action, AbsTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if isinstance(action, AirStrikeTimeoutAction):
            await self.__handleAirStrikeTimeoutAction(action)

        elif isinstance(action, BananaTimeoutAction):
            await self.__handleBananaTimeoutAction(action)

        elif isinstance(action, BasicTimeoutAction):
            await self.__handleBasicTimeoutAction(action)

        elif isinstance(action, GrenadeTimeoutAction):
            await self.__handleGrenadeTimeoutAction(action)

        else:
            raise UnknownTimeoutActionTypeException(f'Encountered unknown AbsTimeoutAction: \"{action}\"')

    def setEventListener(self, listener: TimeoutEventListener | None):
        if listener is not None and not isinstance(listener, TimeoutEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__listener = listener

    def start(self):
        if self.__isStarted:
            self.__timber.log('TimeoutActionMachine', 'Not starting TimeoutActionMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TimeoutActionMachine', 'Starting TimeoutActionMachine...')
        self.__backgroundTaskHelper.createTask(self.__startTimeoutLoop())

    async def __startTimeoutLoop(self):
        while True:
            actions: FrozenList[AbsTimeoutAction] = FrozenList()

            try:
                while not self.__actionQueue.empty():
                    action = self.__actionQueue.get_nowait()
                    actions.append(action)
            except queue.Empty as e:
                self.__timber.log('TimeoutActionMachine', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) (actions size: {len(actions)}): {e}', e, traceback.format_exc())

            actions.freeze()

            for index, action in enumerate(actions):
                try:
                    await self.__handleTimeoutAction(action)
                except Exception as e:
                    self.__timber.log('TimeoutActionMachine', f'Encountered unknown Exception when looping through actions (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}) ({action=}) ({index=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def submitAction(self, action: AbsTimeoutAction):
        if not isinstance(action, AbsTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = 3)
        except queue.Full as e:
            self.__timber.log('TimeoutActionMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())
