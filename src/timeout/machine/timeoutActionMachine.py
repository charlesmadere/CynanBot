import asyncio
import queue
import random
import traceback
from queue import SimpleQueue
from typing import Final

from frozendict import frozendict
from frozenlist import FrozenList

from .timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..exceptions import UnknownTimeoutActionTypeException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.absTimeoutAction import AbsTimeoutAction
from ..models.absTimeoutEvent import AbsTimeoutEvent
from ..models.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.airStrikeTimeoutTarget import AirStrikeTimeoutTarget
from ..models.bananaTimeoutAction import BananaTimeoutAction
from ..models.basicTimeoutAction import BasicTimeoutAction
from ..models.basicTimeoutTarget import BasicTimeoutTarget
from ..models.calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..models.events.airStrikeTimeoutEvent import AirStrikeTimeoutEvent
from ..models.events.bananaTimeoutEvent import BananaTimeoutEvent
from ..models.events.bananaTimeoutFailedTimeoutEvent import BananaTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutEvent import BasicTimeoutEvent
from ..models.events.basicTimeoutFailedTimeoutEvent import BasicTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutTargetUnavailableTimeoutEvent import BasicTimeoutTargetUnavailableTimeoutEvent
from ..models.events.grenadeTimeoutEvent import GrenadeTimeoutEvent
from ..models.events.grenadeTimeoutFailedTimeoutEvent import GrenadeTimeoutFailedTimeoutEvent
from ..models.events.incorrectLiveStatusTimeoutEvent import IncorrectLiveStatusTimeoutEvent
from ..models.events.noAirStrikeInventoryAvailableTimeoutEvent import NoAirStrikeInventoryAvailableTimeoutEvent
from ..models.events.noAirStrikeTargetsAvailableTimeoutEvent import NoAirStrikeTargetsAvailableTimeoutEvent
from ..models.events.noBananaInventoryAvailableTimeoutEvent import NoBananaInventoryAvailableTimeoutEvent
from ..models.events.noBananaTargetAvailableTimeoutEvent import NoBananaTargetAvailableTimeoutEvent
from ..models.events.noGrenadeInventoryAvailableTimeoutEvent import NoGrenadeInventoryAvailableTimeoutEvent
from ..models.events.noGrenadeTargetAvailableTimeoutEvent import NoGrenadeTargetAvailableTimeoutEvent
from ..models.exactTimeoutDuration import ExactTimeoutDuration
from ..models.grenadeTimeoutAction import GrenadeTimeoutAction
from ..models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from ..models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ..timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..useCases.determineAirStrikeTargetsUseCase import DetermineAirStrikeTargetsUseCase
from ..useCases.determineBananaTargetUseCase import DetermineBananaTargetUseCase
from ..useCases.determineExponentialTimeoutDurationSecondsUseCase import \
    DetermineExponentialTimeoutDurationSecondsUseCase
from ..useCases.determineGrenadeTargetUseCase import DetermineGrenadeTargetUseCase
from ..useCases.timeoutRollFailureUseCase import TimeoutRollFailureUseCase
from ...asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ...chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ...chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutActionMachine(TimeoutActionMachineInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        determineBananaTargetUseCase: DetermineBananaTargetUseCase,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        determineAirStrikeTargetsUseCase: DetermineAirStrikeTargetsUseCase,
        determineExponentialTimeoutDurationSecondsUseCase: DetermineExponentialTimeoutDurationSecondsUseCase,
        determineGrenadeTargetUseCase: DetermineGrenadeTargetUseCase,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        timber: TimberInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        timeoutRollFailureUseCase: TimeoutRollFailureUseCase,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 1,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(determineAirStrikeTargetsUseCase, DetermineAirStrikeTargetsUseCase):
            raise TypeError(f'determineAirStrikeTargetsUseCase argument is malformed: \"{determineAirStrikeTargetsUseCase}\"')
        elif not isinstance(determineBananaTargetUseCase, DetermineBananaTargetUseCase):
            raise TypeError(f'determineBananaTargetUseCase argument is malformed: \"{determineBananaTargetUseCase}\"')
        elif not isinstance(determineExponentialTimeoutDurationSecondsUseCase, DetermineExponentialTimeoutDurationSecondsUseCase):
            raise TypeError(f'determineExponentialTimeoutDurationSecondsUseCase argument is malformed: \"{determineExponentialTimeoutDurationSecondsUseCase}\"')
        elif not isinstance(determineGrenadeTargetUseCase, DetermineGrenadeTargetUseCase):
            raise TypeError(f'determineGrenadeTargetUseCase argument is malformed: \"{determineGrenadeTargetUseCase}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(timeoutRollFailureUseCase, TimeoutRollFailureUseCase):
            raise TypeError(f'timeoutRollFailureUseCase argument is malformed: \"{timeoutRollFailureUseCase}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.5 or sleepTimeSeconds > 8:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__asplodieStatsRepository: Final[AsplodieStatsRepositoryInterface] = asplodieStatsRepository
        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__determineAirStrikeTargetsUseCase: Final[DetermineAirStrikeTargetsUseCase] = determineAirStrikeTargetsUseCase
        self.__determineBananaTargetUseCase: Final[DetermineBananaTargetUseCase] = determineBananaTargetUseCase
        self.__determineExponentialTimeoutDurationSecondsUseCase: Final[DetermineExponentialTimeoutDurationSecondsUseCase] = determineExponentialTimeoutDurationSecondsUseCase
        self.__determineGrenadeTargetUseCase: Final[DetermineGrenadeTargetUseCase] = determineGrenadeTargetUseCase
        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__isLiveOnTwitchRepository: Final[IsLiveOnTwitchRepositoryInterface] = isLiveOnTwitchRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__timeoutRollFailureUseCase: Final[TimeoutRollFailureUseCase] = timeoutRollFailureUseCase
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[AbsTimeoutAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[AbsTimeoutEvent]] = SimpleQueue()
        self.__eventListener: TimeoutEventListener | None = None

    async def __calculateTimeoutDuration(self, action: AbsTimeoutAction) -> CalculatedTimeoutDuration:
        timeoutDuration = action.getTimeoutDuration()
        durationSeconds: int

        if isinstance(timeoutDuration, ExactTimeoutDuration):
            durationSeconds = timeoutDuration.seconds

        elif isinstance(timeoutDuration, RandomExponentialTimeoutDuration):
            durationSeconds = await self.__determineExponentialTimeoutDurationSecondsUseCase.invoke(
                timeoutDuration = timeoutDuration,
            )

        elif isinstance(timeoutDuration, RandomLinearTimeoutDuration):
            durationSeconds = random.randint(timeoutDuration.minimumSeconds, timeoutDuration.maximumSeconds)

        else:
            raise ValueError(f'Encountered unknown AbsTimeoutDuration type: \"{timeoutDuration}\"')

        message = utils.secondsToDurationMessage(durationSeconds)

        return CalculatedTimeoutDuration(
            seconds = durationSeconds,
            message = message,
        )

    async def __handleAirStrikeTimeoutAction(self, action: AirStrikeTimeoutAction):
        if not isinstance(action, AirStrikeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not action.ignoreInventory:
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

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        timeoutTargets = await self.__determineAirStrikeTargetsUseCase.invoke(
            timeoutAction = action,
        )

        if len(timeoutTargets) == 0:
            await self.__submitEvent(NoAirStrikeTargetsAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        timeoutDuration = await self.__calculateTimeoutDuration(action)

        timeoutResults: dict[AirStrikeTimeoutTarget, TwitchTimeoutResult] = dict()

        for timeoutTarget in timeoutTargets:
            timeoutResult = await self.__twitchTimeoutHelper.timeout(
                durationSeconds = timeoutDuration.seconds,
                reason = f'{ChatterItemType.AIR_STRIKE.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
                twitchAccessToken = action.moderatorTwitchAccessToken,
                twitchChannelAccessToken = action.userTwitchAccessToken,
                twitchChannelId = action.twitchChannelId,
                userIdToTimeout = timeoutTarget.targetUserId,
                user = action.user,
            )

            timeoutResults[timeoutTarget] = timeoutResult

        frozenTimeoutResults = frozendict(timeoutResults)
        successfulTimeoutTargets: FrozenList[AirStrikeTimeoutTarget] = FrozenList()

        for timeoutTarget, timeoutResult in timeoutResults.items():
            if timeoutResult is TwitchTimeoutResult.SUCCESS:
                successfulTimeoutTargets.append(timeoutTarget)

        successfulTimeoutTargets.freeze()

        if len(successfulTimeoutTargets) == 0:
            await self.__submitEvent(NoAirStrikeTargetsAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.AIR_STRIKE,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(AirStrikeTimeoutEvent(
            originatingAction = action,
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            targets = successfulTimeoutTargets,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            timeoutResults = frozenTimeoutResults,
        ))

    async def __handleBananaTimeoutAction(self, action: BananaTimeoutAction):
        if not isinstance(action, BananaTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.BANANA] < 1:
                await self.__submitEvent(NoBananaInventoryAvailableTimeoutEvent(
                    originatingAction = action,
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                ))
                return

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        timeoutTarget = await self.__determineBananaTargetUseCase.invoke(
            timeoutAction = action,
        )

        if timeoutTarget is None:
            await self.__submitEvent(NoBananaTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        timeoutDuration = await self.__calculateTimeoutDuration(action)

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.BANANA.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = timeoutTarget.targetUserId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(BananaTimeoutFailedTimeoutEvent(
                originatingAction = action,
                target = timeoutTarget,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                timeoutResult = timeoutResult,
            ))
            return

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.BANANA,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(BananaTimeoutEvent(
            originatingAction = action,
            target = timeoutTarget,
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            timeoutResult = timeoutResult,
        ))

    async def __handleBasicTimeoutAction(self, action: BasicTimeoutAction):
        if not isinstance(action, BasicTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        try:
            targetUserName = await self.__requireUserName(
                action = action,
                chatterUserId = action.targetUserId,
            )
        except Exception as e:
            self.__timber.log('TimeoutActionMachine', f'Failed to fetch username for basic timeout target ({action=}): {e}', e, traceback.format_exc())
            await self.__submitEvent(BasicTimeoutTargetUnavailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        timeoutTarget = BasicTimeoutTarget(
            targetUserId = action.targetUserId,
            targetUserName = targetUserName,
        )

        timeoutDuration = await self.__calculateTimeoutDuration(action)

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = action.reason,
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = action.targetUserId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(BasicTimeoutFailedTimeoutEvent(
                originatingAction = action,
                target = timeoutTarget,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                timeoutResult = timeoutResult,
            ))
            return

        await self.__submitEvent(BasicTimeoutEvent(
            originatingAction = action,
            target = timeoutTarget,
            timeoutDuration = timeoutDuration,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            timeoutResult = timeoutResult,
        ))

    async def __handleGrenadeTimeoutAction(self, action: GrenadeTimeoutAction):
        if not isinstance(action, GrenadeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not action.ignoreInventory:
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

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        timeoutTarget = await self.__determineGrenadeTargetUseCase.invoke(
            timeoutAction = action,
        )

        if timeoutTarget is None:
            await self.__submitEvent(NoGrenadeTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        timeoutDuration = await self.__calculateTimeoutDuration(action)

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.GRENADE.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = timeoutTarget.targetUserId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(GrenadeTimeoutFailedTimeoutEvent(
                originatingAction = action,
                target = timeoutTarget,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                timeoutResult = timeoutResult,
            ))
            return

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.GRENADE,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(GrenadeTimeoutEvent(
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            originatingAction = action,
            target = timeoutTarget,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            timeoutResult = timeoutResult,
        ))

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

    async def __requireUserName(
        self,
        action: AbsTimeoutAction,
        chatterUserId: str,
    ) -> str:
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = action.getTwitchChannelId(),
        )

        return await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

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
                        event = self.__eventQueue.get_nowait()
                        events.append(event)
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

    async def __verifyStreamLiveStatus(self, action: AbsTimeoutAction) -> bool:
        streamStatusRequirement = action.getStreamStatusRequirement()

        if streamStatusRequirement is None or streamStatusRequirement is TimeoutStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(
            twitchChannelId = action.getTwitchChannelId(),
        )

        match streamStatusRequirement:
            case TimeoutStreamStatusRequirement.ONLINE: return isLive
            case TimeoutStreamStatusRequirement.OFFLINE: return not isLive
            case _: raise ValueError(f'Encountered unknown TimeoutStreamStatusRequirement value: \"{streamStatusRequirement}\"')
