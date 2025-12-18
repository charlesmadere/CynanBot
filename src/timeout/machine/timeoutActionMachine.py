import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozendict import frozendict
from frozenlist import FrozenList

from .timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..exceptions import BananaTimeoutDiceRollFailedException, ImmuneTimeoutTargetException, \
    UnknownTimeoutActionTypeException, UnknownTimeoutTargetException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ..models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.actions.basicTimeoutAction import BasicTimeoutAction
from ..models.actions.copyAnivMessageTimeoutAction import CopyAnivMessageTimeoutAction
from ..models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..models.actions.tm36TimeoutAction import Tm36TimeoutAction
from ..models.actions.voreTimeoutAction import VoreTimeoutAction
from ..models.events.absTimeoutEvent import AbsTimeoutEvent
from ..models.events.airStrikeTimeoutEvent import AirStrikeTimeoutEvent
from ..models.events.bananaTargetIsImmuneTimeoutEvent import BananaTargetIsImmuneTimeoutEvent
from ..models.events.bananaTimeoutDiceRollFailedEvent import BananaTimeoutDiceRollFailedEvent
from ..models.events.bananaTimeoutDiceRollQueuedEvent import BananaTimeoutDiceRollQueuedEvent
from ..models.events.bananaTimeoutEvent import BananaTimeoutEvent
from ..models.events.bananaTimeoutFailedTimeoutEvent import BananaTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutEvent import BasicTimeoutEvent
from ..models.events.basicTimeoutFailedTimeoutEvent import BasicTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutTargetUnavailableTimeoutEvent import BasicTimeoutTargetUnavailableTimeoutEvent
from ..models.events.copyAnivMessageTimeoutEvent import CopyAnivMessageTimeoutEvent
from ..models.events.copyAnivMessageTimeoutFailedTimeoutEvent import CopyAnivMessageTimeoutFailedTimeoutEvent
from ..models.events.grenadeTimeoutEvent import GrenadeTimeoutEvent
from ..models.events.grenadeTimeoutFailedTimeoutEvent import GrenadeTimeoutFailedTimeoutEvent
from ..models.events.incorrectLiveStatusTimeoutEvent import IncorrectLiveStatusTimeoutEvent
from ..models.events.noAirStrikeInventoryAvailableTimeoutEvent import NoAirStrikeInventoryAvailableTimeoutEvent
from ..models.events.noAirStrikeTargetsAvailableTimeoutEvent import NoAirStrikeTargetsAvailableTimeoutEvent
from ..models.events.noBananaInventoryAvailableTimeoutEvent import NoBananaInventoryAvailableTimeoutEvent
from ..models.events.noBananaTargetAvailableTimeoutEvent import NoBananaTargetAvailableTimeoutEvent
from ..models.events.noGrenadeInventoryAvailableTimeoutEvent import NoGrenadeInventoryAvailableTimeoutEvent
from ..models.events.noGrenadeTargetAvailableTimeoutEvent import NoGrenadeTargetAvailableTimeoutEvent
from ..models.events.noTm36InventoryAvailableTimeoutEvent import NoTm36InventoryAvailableTimeoutEvent
from ..models.events.noVoreInventoryAvailableTimeoutEvent import NoVoreInventoryAvailableTimeoutEvent
from ..models.events.noVoreTargetAvailableTimeoutEvent import NoVoreTargetAvailableTimeoutEvent
from ..models.events.tm36TimeoutEvent import Tm36TimeoutEvent
from ..models.events.tm36TimeoutFailedTimeoutEvent import Tm36TimeoutFailedTimeoutEvent
from ..models.events.voreTargetIsImmuneTimeoutEvent import VoreTargetIsImmuneTimeoutEvent
from ..models.events.voreTimeoutEvent import VoreTimeoutEvent
from ..models.events.voreTimeoutFailedTimeoutEvent import VoreTimeoutFailedTimeoutEvent
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..models.timeoutTarget import TimeoutTarget
from ..repositories.chatterTimeoutHistoryRepositoryInterface import ChatterTimeoutHistoryRepositoryInterface
from ..useCases.calculateTimeoutDurationUseCase import CalculateTimeoutDurationUseCase
from ..useCases.determineAirStrikeTargetsUseCase import DetermineAirStrikeTargetsUseCase
from ..useCases.determineBananaTargetUseCase import DetermineBananaTargetUseCase
from ..useCases.determineGrenadeTargetUseCase import DetermineGrenadeTargetUseCase
from ..useCases.determineTimeoutTargetUseCase import DetermineTimeoutTargetUseCase
from ..useCases.determineTm36SplashTargetUseCase import DetermineTm36SplashTargetUseCase
from ...aniv.repositories.anivCopyMessageTimeoutScoreRepositoryInterface import \
    AnivCopyMessageTimeoutScoreRepositoryInterface
from ...asplodieStats.models.asplodieStats import AsplodieStats
from ...asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ...chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ...chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...pixelsDice.machine.pixelsDiceMachineInterface import PixelsDiceMachineInterface
from ...pixelsDice.models.diceRollRequest import DiceRollRequest
from ...pixelsDice.models.diceRollResult import DiceRollResult
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutActionMachine(TimeoutActionMachineInterface):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        calculateTimeoutDurationUseCase: CalculateTimeoutDurationUseCase,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterTimeoutHistoryRepository: ChatterTimeoutHistoryRepositoryInterface,
        determineAirStrikeTargetsUseCase: DetermineAirStrikeTargetsUseCase,
        determineBananaTargetUseCase: DetermineBananaTargetUseCase,
        determineGrenadeTargetUseCase: DetermineGrenadeTargetUseCase,
        determineTimeoutTargetUseCase: DetermineTimeoutTargetUseCase,
        determineTm36SplashTargetUseCase: DetermineTm36SplashTargetUseCase,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        pixelsDiceMachine: PixelsDiceMachineInterface | None,
        timber: TimberInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(calculateTimeoutDurationUseCase, CalculateTimeoutDurationUseCase):
            raise TypeError(f'calculateTimeoutDurationUseCase argument is malformed: \"{calculateTimeoutDurationUseCase}\"')
        elif not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterTimeoutHistoryRepository, ChatterTimeoutHistoryRepositoryInterface):
            raise TypeError(f'chatterTimeoutHistoryRepository argument is malformed: \"{chatterTimeoutHistoryRepository}\"')
        elif not isinstance(determineAirStrikeTargetsUseCase, DetermineAirStrikeTargetsUseCase):
            raise TypeError(f'determineAirStrikeTargetsUseCase argument is malformed: \"{determineAirStrikeTargetsUseCase}\"')
        elif not isinstance(determineBananaTargetUseCase, DetermineBananaTargetUseCase):
            raise TypeError(f'determineBananaTargetUseCase argument is malformed: \"{determineBananaTargetUseCase}\"')
        elif not isinstance(determineGrenadeTargetUseCase, DetermineGrenadeTargetUseCase):
            raise TypeError(f'determineGrenadeTargetUseCase argument is malformed: \"{determineGrenadeTargetUseCase}\"')
        elif not isinstance(determineTimeoutTargetUseCase, DetermineTimeoutTargetUseCase):
            raise TypeError(f'determineTimeoutTargetUseCase argument is malformed: \"{determineTimeoutTargetUseCase}\"')
        elif not isinstance(determineTm36SplashTargetUseCase, DetermineTm36SplashTargetUseCase):
            raise TypeError(f'determineTm36SplashTargetUseCase argument is malformed: \"{determineTm36SplashTargetUseCase}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif pixelsDiceMachine is not None and not isinstance(pixelsDiceMachine, PixelsDiceMachineInterface):
            raise TypeError(f'pixelsDiceMachine argument is malformed: \"{pixelsDiceMachine}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
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

        self.__anivCopyMessageTimeoutScoreRepository: Final[AnivCopyMessageTimeoutScoreRepositoryInterface] = anivCopyMessageTimeoutScoreRepository
        self.__asplodieStatsRepository: Final[AsplodieStatsRepositoryInterface] = asplodieStatsRepository
        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__calculateTimeoutDurationUseCase: Final[CalculateTimeoutDurationUseCase] = calculateTimeoutDurationUseCase
        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterTimeoutHistoryRepository: Final[ChatterTimeoutHistoryRepositoryInterface] = chatterTimeoutHistoryRepository
        self.__determineAirStrikeTargetsUseCase: Final[DetermineAirStrikeTargetsUseCase] = determineAirStrikeTargetsUseCase
        self.__determineBananaTargetUseCase: Final[DetermineBananaTargetUseCase] = determineBananaTargetUseCase
        self.__determineGrenadeTargetUseCase: Final[DetermineGrenadeTargetUseCase] = determineGrenadeTargetUseCase
        self.__determineTimeoutTargetUseCase: Final[DetermineTimeoutTargetUseCase] = determineTimeoutTargetUseCase
        self.__determineTm36SplashTargetUseCase: Final[DetermineTm36SplashTargetUseCase] = determineTm36SplashTargetUseCase
        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__isLiveOnTwitchRepository: Final[IsLiveOnTwitchRepositoryInterface] = isLiveOnTwitchRepository
        self.__pixelsDiceMachine: Final[PixelsDiceMachineInterface | None] = pixelsDiceMachine
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[AbsTimeoutAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[AbsTimeoutEvent]] = SimpleQueue()
        self.__eventListener: TimeoutEventListener | None = None

    async def __handleAirStrikeTimeoutAction(self, action: AirStrikeTimeoutAction):
        if not isinstance(action, AirStrikeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.AIR_STRIKE] < 1:
                await self.__submitEvent(NoAirStrikeInventoryAvailableTimeoutEvent(
                    originatingAction = action,
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                    instigatorUserName = instigatorUserName,
                ))
                return

        timeoutTargets = await self.__determineAirStrikeTargetsUseCase.invoke(
            timeoutAction = action,
        )

        if len(timeoutTargets) == 0:
            await self.__submitEvent(NoAirStrikeTargetsAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
            ))
            return

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResults: dict[TimeoutTarget, TwitchTimeoutResult] = dict()

        for timeoutTarget in timeoutTargets:
            timeoutResults[timeoutTarget] = await self.__twitchTimeoutHelper.timeout(
                durationSeconds = timeoutDuration.seconds,
                reason = f'{ChatterItemType.AIR_STRIKE.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
                twitchAccessToken = action.moderatorTwitchAccessToken,
                twitchChannelAccessToken = action.userTwitchAccessToken,
                twitchChannelId = action.twitchChannelId,
                userIdToTimeout = timeoutTarget.userId,
                user = action.user,
            )

        frozenTimeoutResults: frozendict[TimeoutTarget, TwitchTimeoutResult] = frozendict(timeoutResults)
        successfulTimeoutTargets: FrozenList[TimeoutTarget] = FrozenList()
        asplodieStats: dict[TimeoutTarget, AsplodieStats] = dict()

        for timeoutTarget, timeoutResult in timeoutResults.items():
            if timeoutResult is TwitchTimeoutResult.SUCCESS:
                successfulTimeoutTargets.append(timeoutTarget)

                asplodieStats[timeoutTarget] = await self.__asplodieStatsRepository.addAsplodie(
                    isSelfAsplodie = timeoutTarget.userId == action.instigatorUserId,
                    durationAsplodiedSeconds = timeoutDuration.seconds,
                    chatterUserId = timeoutTarget.userId,
                    twitchChannelId = action.twitchChannelId,
                )

        successfulTimeoutTargets.freeze()
        frozenAsplodieStats: frozendict[TimeoutTarget, AsplodieStats] = frozendict(asplodieStats)

        if len(successfulTimeoutTargets) == 0:
            await self.__submitEvent(NoAirStrikeTargetsAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
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
            asplodieStats = frozenAsplodieStats,
            timeoutResults = frozenTimeoutResults,
            targets = successfulTimeoutTargets,
            bombEmote = await self.__trollmojiHelper.getBombEmoteOrBackup(),
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            explodedEmote = await self.__trollmojiHelper.getExplodedEmoteOrBackup(),
            instigatorUserName = instigatorUserName,
        ))

    async def __handleBananaTimeoutAction(self, action: BananaTimeoutAction):
        if not isinstance(action, BananaTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.BANANA] < 1:
                await self.__submitEvent(NoBananaInventoryAvailableTimeoutEvent(
                    originatingAction = action,
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                    instigatorUserName = instigatorUserName,
                ))
                return

        try:
            timeoutTarget = await self.__determineTimeoutTargetUseCase.invoke(
                timeoutAction = action,
            )
        except ImmuneTimeoutTargetException as e:
            await self.__submitEvent(BananaTargetIsImmuneTimeoutEvent(
                timeoutTarget = e.timeoutTarget,
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return
        except UnknownTimeoutTargetException as e:
            self.__timber.log('TimeoutActionMachine', f'Failed to determine banana timeout target ({action=}): {e}', e, traceback.format_exc())
            await self.__submitEvent(NoBananaTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
            ))
            return

        if action.useDiceRoll and self.__pixelsDiceMachine is not None and self.__pixelsDiceMachine.isConnected:
            async def onDiceRolled(result: DiceRollResult):
                await self.__handleBananaTimeoutActionEnding(
                    action = action,
                    timeoutTarget = timeoutTarget,
                    roll = result.roll,
                    instigatorUserName = instigatorUserName,
                )

            requestQueueSize = self.__pixelsDiceMachine.submitRequest(DiceRollRequest(
                callback = onDiceRolled,
                twitchChannelId = action.twitchChannelId,
            ))

            await self.__submitEvent(BananaTimeoutDiceRollQueuedEvent(
                timeoutTarget = timeoutTarget,
                originatingAction = action,
                requestQueueSize = requestQueueSize,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
            ))
        else:
            await self.__handleBananaTimeoutActionEnding(
                action = action,
                timeoutTarget = timeoutTarget,
                roll = None,
                instigatorUserName = instigatorUserName,
            )

    async def __handleBananaTimeoutActionEnding(
        self,
        action: BananaTimeoutAction,
        roll: int | None,
        instigatorUserName: str,
        timeoutTarget: TimeoutTarget,
    ):
        diceRoll: TimeoutDiceRoll | None = None

        if roll is not None:
            diceRoll = TimeoutDiceRoll(
                dieSize = 20,
                roll = roll,
            )

        try:
            timeoutData = await self.__determineBananaTargetUseCase.invoke(
                timeoutTarget = timeoutTarget,
                timeoutAction = action,
                instigatorUserName = instigatorUserName,
                diceRoll = diceRoll,
            )
        except BananaTimeoutDiceRollFailedException as e:
            await self.__submitEvent(BananaTimeoutDiceRollFailedEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
                diceRoll = e.diceRoll,
                diceRollFailureData = e.diceRollFailureData,
                timeoutTarget = e.timeoutTarget,
            ))
            return
        except UnknownTimeoutTargetException as e:
            self.__timber.log('TimeoutActionMachine', f'Failed to determine banana timeout target ({action=}): {e}', e, traceback.format_exc())
            await self.__submitEvent(NoBananaTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
            ))
            return

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.BANANA.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = timeoutData.timeoutTarget.userId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(BananaTimeoutFailedTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                timeoutTarget = timeoutData.timeoutTarget,
                timeoutResult = timeoutResult,
            ))
            return

        asplodieStats = await self.__asplodieStatsRepository.addAsplodie(
            isSelfAsplodie = timeoutData.timeoutTarget.userId == action.instigatorUserId,
            durationAsplodiedSeconds = timeoutDuration.seconds,
            chatterUserId = timeoutData.timeoutTarget.userId,
            twitchChannelId = action.twitchChannelId,
        )

        chatterTimeoutHistory = await self.__chatterTimeoutHistoryRepository.add(
            durationSeconds = timeoutDuration.seconds,
            chatterUserId = timeoutData.timeoutTarget.userId,
            timedOutByUserId = action.instigatorUserId,
            twitchChannelId = action.twitchChannelId,
        )

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.BANANA,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(BananaTimeoutEvent(
            asplodieStats = asplodieStats,
            originatingAction = action,
            isReverse = timeoutData.isReverse,
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            chatterTimeoutHistory = chatterTimeoutHistory,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            instigatorUserName = instigatorUserName,
            ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
            diceRoll = timeoutData.diceRoll,
            diceRollFailureData = timeoutData.diceRollFailureData,
            timeoutTarget = timeoutData.timeoutTarget,
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

        timeoutTarget = TimeoutTarget(
            userId = action.targetUserId,
            userName = targetUserName,
        )

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

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
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                timeoutTarget = timeoutTarget,
                timeoutResult = timeoutResult,
            ))
            return

        await self.__submitEvent(BasicTimeoutEvent(
            originatingAction = action,
            timeoutDuration = timeoutDuration,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            timeoutTarget = timeoutTarget,
            timeoutResult = timeoutResult,
        ))

    async def __handleCopyAnivMessageTimeoutAction(self, action: CopyAnivMessageTimeoutAction):
        if not isinstance(action, CopyAnivMessageTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        anivUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.anivUserId,
        )

        targetUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.targetUserId,
        )

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'Timeout for copying {anivUserName}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = action.targetUserId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(CopyAnivMessageTimeoutFailedTimeoutEvent(
                originatingAction = action,
                anivUserName = anivUserName,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                targetUserName = targetUserName,
                timeoutResult = timeoutResult,
            ))
            return

        copyMessageTimeoutScore = await self.__anivCopyMessageTimeoutScoreRepository.incrementTimeoutScore(
            timeoutDurationSeconds = timeoutDuration.seconds,
            chatterUserId = action.targetUserId,
            twitchChannelId = action.twitchChannelId,
        )

        await self.__submitEvent(CopyAnivMessageTimeoutEvent(
            copyMessageTimeoutScore = copyMessageTimeoutScore,
            originatingAction = action,
            timeoutDuration = timeoutDuration,
            anivUserName = anivUserName,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
            targetUserName = targetUserName,
            timeoutResult = timeoutResult,
        ))

    async def __handleGrenadeTimeoutAction(self, action: GrenadeTimeoutAction):
        if not isinstance(action, GrenadeTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.GRENADE] < 1:
                await self.__submitEvent(NoGrenadeInventoryAvailableTimeoutEvent(
                    originatingAction = action,
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                    instigatorUserName = instigatorUserName,
                ))
                return

        timeoutTarget = await self.__determineGrenadeTargetUseCase.invoke(
            timeoutAction = action,
        )

        if timeoutTarget is None:
            await self.__submitEvent(NoGrenadeTargetAvailableTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                thumbsDownEmote = await self.__trollmojiHelper.getThumbsDownEmoteOrBackup(),
            ))
            return

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.GRENADE.humanName} timeout from {instigatorUserName} for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = timeoutTarget.userId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(GrenadeTimeoutFailedTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                timeoutTarget = timeoutTarget,
                timeoutResult = timeoutResult,
            ))
            return

        asplodieStats = await self.__asplodieStatsRepository.addAsplodie(
            isSelfAsplodie = timeoutTarget.userId == action.instigatorUserId,
            durationAsplodiedSeconds = timeoutDuration.seconds,
            chatterUserId = timeoutTarget.userId,
            twitchChannelId = action.twitchChannelId,
        )

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.GRENADE,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(GrenadeTimeoutEvent(
            asplodieStats = asplodieStats,
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            originatingAction = action,
            bombEmote = await self.__trollmojiHelper.getBombEmoteOrBackup(),
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            explodedEmote = await self.__trollmojiHelper.getExplodedEmoteOrBackup(),
            instigatorUserName = instigatorUserName,
            timeoutTarget = timeoutTarget,
            timeoutResult = timeoutResult,
        ))

    async def __handleTimeoutAction(self, action: AbsTimeoutAction):
        if not isinstance(action, AbsTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if isinstance(action, AirStrikeTimeoutAction):
            await self.__handleAirStrikeTimeoutAction(
                action = action,
            )

        elif isinstance(action, BananaTimeoutAction):
            await self.__handleBananaTimeoutAction(
                action = action,
            )

        elif isinstance(action, BasicTimeoutAction):
            await self.__handleBasicTimeoutAction(
                action = action,
            )

        elif isinstance(action, CopyAnivMessageTimeoutAction):
            await self.__handleCopyAnivMessageTimeoutAction(
                action = action,
            )

        elif isinstance(action, GrenadeTimeoutAction):
            await self.__handleGrenadeTimeoutAction(
                action = action,
            )

        elif isinstance(action, Tm36TimeoutAction):
            await self.__handleTm36TimeoutAction(
                action = action,
            )

        elif isinstance(action, VoreTimeoutAction):
            await self.__handleVoreTimeoutAction(
                action = action,
            )

        else:
            raise UnknownTimeoutActionTypeException(f'Encountered unknown AbsTimeoutAction: \"{action}\"')

    async def __handleTm36TimeoutAction(self, action: Tm36TimeoutAction):
        if not isinstance(action, Tm36TimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        targetUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.targetUserId,
        )

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.targetUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.TM_36] < 1:
                await self.__submitEvent(NoTm36InventoryAvailableTimeoutEvent(
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                    targetUserName = targetUserName,
                    thumbsDownEmote = await self.__trollmojiHelper.getThumbsDownEmoteOrBackup(),
                    originatingAction = action,
                ))
                return

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.TM_36.humanName} timeout for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = action.targetUserId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(Tm36TimeoutFailedTimeoutEvent(
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                targetUserName = targetUserName,
                originatingAction = action,
                timeoutResult = timeoutResult,
            ))
            return

        splashTimeoutTarget = await self.__determineTm36SplashTargetUseCase.invoke(
            timeoutAction = action,
        )

        if splashTimeoutTarget is not None:
            splashTimeoutResult = await self.__twitchTimeoutHelper.timeout(
                durationSeconds = timeoutDuration.seconds,
                reason = f'Hit by {ChatterItemType.TM_36.humanName} splash damage timeout from {targetUserName}',
                twitchAccessToken = action.moderatorTwitchAccessToken,
                twitchChannelAccessToken = action.userTwitchAccessToken,
                twitchChannelId = action.twitchChannelId,
                userIdToTimeout = action.targetUserId,
                user = action.user,
            )

            if splashTimeoutResult is TwitchTimeoutResult.SUCCESS:
                await self.__asplodieStatsRepository.addAsplodie(
                    isSelfAsplodie = False,
                    durationAsplodiedSeconds = timeoutDuration.seconds,
                    chatterUserId = splashTimeoutTarget.userId,
                    twitchChannelId = action.twitchChannelId,
                )
            else:
                splashTimeoutTarget = None

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.TM_36,
                giveAmount = -1,
                chatterUserId = action.targetUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(Tm36TimeoutEvent(
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            originatingAction = action,
            bombEmote = await self.__trollmojiHelper.getBombEmoteOrBackup(),
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            explodedEmote = await self.__trollmojiHelper.getExplodedEmoteOrBackup(),
            targetUserName = targetUserName,
            splashTimeoutTarget = splashTimeoutTarget,
            timeoutResult = timeoutResult,
        ))

    async def __handleVoreTimeoutAction(self, action: VoreTimeoutAction):
        if not isinstance(action, VoreTimeoutAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__verifyStreamLiveStatus(action):
            await self.__submitEvent(IncorrectLiveStatusTimeoutEvent(
                originatingAction = action,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
            ))
            return

        instigatorUserName = await self.__requireUserName(
            action = action,
            chatterUserId = action.instigatorUserId,
        )

        try:
            timeoutTarget = await self.__determineTimeoutTargetUseCase.invoke(
                timeoutAction = action,
            )
        except ImmuneTimeoutTargetException as e:
            self.__timber.log('TimeoutActionMachine', f'Vore target is immune ({action=})', e, traceback.format_exc())
            await self.__submitEvent(VoreTargetIsImmuneTimeoutEvent(
                timeoutTarget = e.timeoutTarget,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return
        except UnknownTimeoutTargetException as e:
            self.__timber.log('TimeoutActionMachine', f'Failed to determine vore target ({action=})', e, traceback.format_exc())
            await self.__submitEvent(NoVoreTargetAvailableTimeoutEvent(
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                originatingAction = action,
            ))
            return

        if not action.ignoreInventory:
            inventory = await self.__chatterInventoryHelper.get(
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if inventory[ChatterItemType.VORE] < 1:
                await self.__submitEvent(NoVoreInventoryAvailableTimeoutEvent(
                    timeoutTarget = timeoutTarget,
                    eventId = await self.__timeoutIdGenerator.generateEventId(),
                    thumbsDownEmote = await self.__trollmojiHelper.getThumbsDownEmoteOrBackup(),
                    originatingAction = action,
                ))
                return

        timeoutDuration = await self.__calculateTimeoutDurationUseCase.invoke(
            timeoutAction = action,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutDuration.seconds,
            reason = f'{ChatterItemType.VORE.humanName} timeout for {timeoutDuration.message}',
            twitchAccessToken = action.moderatorTwitchAccessToken,
            twitchChannelAccessToken = action.userTwitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userIdToTimeout = timeoutTarget.userId,
            user = action.user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            await self.__submitEvent(VoreTimeoutFailedTimeoutEvent(
                timeoutTarget = timeoutTarget,
                eventId = await self.__timeoutIdGenerator.generateEventId(),
                instigatorUserName = instigatorUserName,
                timeoutResult = timeoutResult,
                originatingAction = action,
            ))
            return

        asplodieStats = await self.__asplodieStatsRepository.addAsplodie(
            isSelfAsplodie = timeoutTarget.userId == action.instigatorUserId,
            durationAsplodiedSeconds = timeoutDuration.seconds,
            chatterUserId = timeoutTarget.userId,
            twitchChannelId = action.twitchChannelId,
        )

        chatterTimeoutHistory = await self.__chatterTimeoutHistoryRepository.add(
            durationSeconds = timeoutDuration.seconds,
            chatterUserId = timeoutTarget.userId,
            timedOutByUserId = action.instigatorUserId,
            twitchChannelId = action.twitchChannelId,
        )

        updatedInventory: ChatterItemGiveResult | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryHelper.give(
                itemType = ChatterItemType.VORE,
                giveAmount = -1,
                chatterUserId = action.instigatorUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(VoreTimeoutEvent(
            asplodieStats = asplodieStats,
            timeoutTarget = timeoutTarget,
            timeoutDuration = timeoutDuration,
            updatedInventory = updatedInventory,
            chatterTimeoutHistory = chatterTimeoutHistory,
            eventId = await self.__timeoutIdGenerator.generateEventId(),
            instigatorUserName = instigatorUserName,
            ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
            timeoutResult = timeoutResult,
            originatingAction = action,
        ))

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
                self.__timber.log('TimeoutActionMachine', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}): {e}', e, traceback.format_exc())

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
