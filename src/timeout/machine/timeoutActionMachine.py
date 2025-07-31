import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..exceptions import UnknownTimeoutActionTypeException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.absTimeoutAction import AbsTimeoutAction
from ..models.absTimeoutEvent import AbsTimeoutEvent
from ..models.airStrikeTargetData import AirStrikeTargetData
from ..models.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.bananaTimeoutAction import BananaTimeoutAction
from ..models.basicTimeoutAction import BasicTimeoutAction
from ..models.events.noAirStrikeInventoryAvailableTimeoutEvent import NoAirStrikeInventoryAvailableTimeoutEvent
from ..models.events.noAirStrikeTargetsAvailableTimeoutEvent import NoAirStrikeTargetsAvailableTimeoutEvent
from ..models.events.noGrenadeInventoryAvailableTimeoutEvent import NoGrenadeInventoryAvailableTimeoutEvent
from ..models.events.noGrenadeTargetAvailableTimeoutEvent import NoGrenadeTargetAvailableTimeoutEvent
from ..models.grenadeTimeoutAction import GrenadeTimeoutAction
from ..useCases.determineAirStrikeTargetsUseCase import DetermineAirStrikeTargetsUseCase
from ..useCases.determineGrenadeTargetUseCase import DetermineGrenadeTargetUseCase
from ..useCases.timeoutRollFailureUseCase import TimeoutRollFailureUseCase
from ...chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ...chatterInventory.models.chatterItemType import ChatterItemType
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
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        determineAirStrikeTargetsUseCase: DetermineAirStrikeTargetsUseCase,
        determineGrenadeTargetUseCase: DetermineGrenadeTargetUseCase,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        timber: TimberInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        timeoutRollFailureUseCase: TimeoutRollFailureUseCase,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        sleepTimeSeconds: float = 1,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(determineAirStrikeTargetsUseCase, DetermineAirStrikeTargetsUseCase):
            raise TypeError(f'determineAirStrikeTargetsUseCase argument is malformed: \"{determineAirStrikeTargetsUseCase}\"')
        elif not isinstance(determineGrenadeTargetUseCase, DetermineGrenadeTargetUseCase):
            raise TypeError(f'determineGrenadeTargetUseCase argument is malformed: \"{determineGrenadeTargetUseCase}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(timeoutRollFailureUseCase, TimeoutRollFailureUseCase):
            raise TypeError(f'timeoutRollFailureUseCase argument is malformed: \"{timeoutRollFailureUseCase}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.5 or sleepTimeSeconds > 8:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__determineAirStrikeTargetsUseCase: Final[DetermineAirStrikeTargetsUseCase] = determineAirStrikeTargetsUseCase
        self.__determineGrenadeTargetUseCase: Final[DetermineGrenadeTargetUseCase] = determineGrenadeTargetUseCase
        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__timeoutRollFailureUseCase: Final[TimeoutRollFailureUseCase] = timeoutRollFailureUseCase
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[AbsTimeoutAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[AbsTimeoutEvent]] = SimpleQueue()
        self.__eventListener: TimeoutEventListener | None = None

    async def __handleAirStrikeTimeoutAction(self, action: AirStrikeTimeoutAction):
        if not isinstance(action, AirStrikeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        inventory = await self.__chatterInventoryHelper.get(
            chatterUserId = action.instigatorUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if inventory[ChatterItemType.AIR_STRIKE] < 1:
            await self.__submitEvent(NoAirStrikeInventoryAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        airStrikeTargets = await self.__determineAirStrikeTargetsUseCase.invoke(
            timeoutAction = action,
        )

        frozenAirStrikeTargets: FrozenList[AirStrikeTargetData] = FrozenList(airStrikeTargets)
        frozenAirStrikeTargets.freeze()

        if len(frozenAirStrikeTargets) == 0:
            await self.__submitEvent(NoAirStrikeTargetsAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

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

        inventory = await self.__chatterInventoryHelper.get(
            chatterUserId = action.instigatorUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if inventory[ChatterItemType.GRENADE] < 1:
            await self.__submitEvent(NoGrenadeInventoryAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        grenadeTarget = await self.__determineGrenadeTargetUseCase.invoke(
            timeoutAction = action,
        )

        if grenadeTarget is None:
            await self.__submitEvent(NoGrenadeTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

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

        self.__eventListener = listener

    def start(self):
        if self.__isStarted:
            self.__timber.log('TimeoutActionMachine', 'Not starting TimeoutActionMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TimeoutActionMachine', 'Starting TimeoutActionMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startActionLoop(self):
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
                    self.__timber.log('TimeoutActionMachine', f'Encountered unknown Exception when looping through actions (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}) ({index=}) ({action=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: FrozenList[AbsTimeoutEvent] = FrozenList()

                try:
                    while not self.__eventQueue.empty():
                        events.append(self.__eventQueue.get_nowait())
                except queue.Empty as e:
                    self.__timber.log('TimeoutActionMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({events=}): {e}', e, traceback.format_exc())

                events.freeze()

                for index, event in enumerate(events):
                    try:
                        await eventListener.onNewTimeoutEvent(event)
                    except Exception as e:
                        self.__timber.log('TimeoutActionMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({index=}) ({event=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def submitAction(self, action: AbsTimeoutAction):
        if not isinstance(action, AbsTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TimeoutActionMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitEvent(self, event: AbsTimeoutEvent):
        if not isinstance(event, AbsTimeoutEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TimeoutActionMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
