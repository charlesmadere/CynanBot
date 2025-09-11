import asyncio
import queue
import traceback
from dataclasses import dataclass
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..exceptions import UnknownChatterItemTypeException
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ..models.absChatterItemAction import AbsChatterItemAction
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.events.absChatterItemEvent import AbsChatterItemEvent
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.notEnoughInventoryChatterItemEvent import NotEnoughInventoryChatterItemEvent
from ..models.events.useAirStrikeChatterItemEvent import UseAirStrikeChatterItemEvent
from ..models.events.useBananaChatterItemEvent import UseBananaChatterItemEvent
from ..models.events.useCassetteTapeChatterItemEvent import UseCassetteTapeChatterItemEvent
from ..models.events.useGrenadeChatterItemEvent import UseGrenadeChatterItemEvent
from ..models.tradeChatterItemAction import TradeChatterItemAction
from ..models.useChatterItemAction import UseChatterItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ...timeout.models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ...timeout.models.actions.bananaTimeoutAction import BananaTimeoutAction
from ...timeout.models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ...timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from ...timeout.models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class ChatterInventoryItemUseMachine(ChatterInventoryItemUseMachineInterface):

    @dataclass(frozen = True)
    class TokensAndDetails:
        moderatorTwitchAccessToken: str
        moderatorUserId: str
        userTwitchAccessToken: str

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
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
        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[AbsChatterItemAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[AbsChatterItemEvent]] = SimpleQueue()
        self.__eventListener: ChatterItemEventListener | None = None

    async def __fetchTokensAndDetails(
        self,
        twitchChannelId: str,
    ) -> TokensAndDetails:
        userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken,
        )

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = moderatorUserId,
        )

        return ChatterInventoryItemUseMachine.TokensAndDetails(
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userTwitchAccessToken = userTwitchAccessToken,
        )

    async def __handleAirStrikeItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getAirStrikeItemDetails()

        timeoutDuration: AbsTimeoutDuration = RandomLinearTimeoutDuration(
            maximumSeconds = itemDetails.maxDurationSeconds,
            minimumSeconds = itemDetails.minDurationSeconds,
        )

        tokensAndDetails = await self.__fetchTokensAndDetails(
            twitchChannelId = action.twitchChannelId,
        )

        self.__timeoutActionMachine.submitAction(AirStrikeTimeoutAction(
            timeoutDuration = timeoutDuration,
            ignoreInventory = action.ignoreInventory,
            maxTimeoutTargets = itemDetails.maxTargets,
            minTimeoutTargets = itemDetails.minTargets,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            instigatorUserId = action.chatterUserId,
            moderatorTwitchAccessToken = tokensAndDetails.moderatorTwitchAccessToken,
            moderatorUserId = tokensAndDetails.moderatorUserId,
            twitchChannelId = action.twitchChannelId,
            twitchChatMessageId = action.twitchChatMessageId,
            userTwitchAccessToken = tokensAndDetails.userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = action.user,
        ))

        await self.__submitEvent(UseAirStrikeChatterItemEvent(
            itemDetails = itemDetails,
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            originatingAction = action,
        ))

    async def __handleBananaItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getBananaItemDetails()

        timeoutDuration: AbsTimeoutDuration = ExactTimeoutDuration(
            seconds = itemDetails.durationSeconds,
        )

        tokensAndDetails = await self.__fetchTokensAndDetails(
            twitchChannelId = action.twitchChannelId,
        )

        self.__timeoutActionMachine.submitAction(BananaTimeoutAction(
            timeoutDuration = timeoutDuration,
            ignoreInventory = action.ignoreInventory,
            isRandomChanceEnabled = itemDetails.randomChanceEnabled,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            chatMessage = action.chatMessage,
            instigatorUserId = action.chatterUserId,
            moderatorTwitchAccessToken = tokensAndDetails.moderatorTwitchAccessToken,
            moderatorUserId = tokensAndDetails.moderatorUserId,
            twitchChannelId = action.twitchChannelId,
            twitchChatMessageId = action.twitchChatMessageId,
            userTwitchAccessToken = tokensAndDetails.userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = action.user,
        ))

        await self.__submitEvent(UseBananaChatterItemEvent(
            itemDetails = itemDetails,
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            originatingAction = action,
        ))

    async def __handleCassetteTapeItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        # TODO
        pass

        await self.__submitEvent(UseCassetteTapeChatterItemEvent(
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            originatingAction = action,
        ))

    async def __handleGrenadeItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getGrenadeItemDetails()

        timeoutDuration: AbsTimeoutDuration = RandomLinearTimeoutDuration(
            maximumSeconds = itemDetails.maxDurationSeconds,
            minimumSeconds = itemDetails.minDurationSeconds,
        )

        tokensAndDetails = await self.__fetchTokensAndDetails(
            twitchChannelId = action.twitchChannelId,
        )

        self.__timeoutActionMachine.submitAction(GrenadeTimeoutAction(
            timeoutDuration = timeoutDuration,
            ignoreInventory = action.ignoreInventory,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            instigatorUserId = action.chatterUserId,
            moderatorTwitchAccessToken = tokensAndDetails.moderatorTwitchAccessToken,
            moderatorUserId = tokensAndDetails.moderatorUserId,
            twitchChannelId = action.twitchChannelId,
            twitchChatMessageId = action.twitchChatMessageId,
            userTwitchAccessToken = tokensAndDetails.userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = action.user,
        ))

        await self.__submitEvent(UseGrenadeChatterItemEvent(
            itemDetails = itemDetails,
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            originatingAction = action,
        ))

    async def __handleItemAction(self, action: AbsChatterItemAction):
        if not isinstance(action, AbsChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if isinstance(action, TradeChatterItemAction):
            pass

        elif isinstance(action, UseChatterItemAction):
            pass

        else:
            raise RuntimeError()

    async def __handleUseItemAction(self, action: UseChatterItemAction):
        if not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            await self.__submitEvent(DisabledFeatureChatterItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return
        elif action.itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
            await self.__submitEvent(DisabledItemTypeChatterItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return

        chatterInventory: ChatterInventoryData | None = None

        if not action.ignoreInventory:
            chatterInventory = await self.__chatterInventoryRepository.get(
                chatterUserId = action.chatterUserId,
                twitchChannelId = action.twitchChannelId,
            )

            if chatterInventory[action.itemType] < 1:
                await self.__submitEvent(NotEnoughInventoryChatterItemEvent(
                    chatterInventory = chatterInventory,
                    eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                    originatingAction = action,
                ))
                return

        match action.itemType:
            case ChatterItemType.AIR_STRIKE:
                await self.__handleAirStrikeItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.BANANA:
                await self.__handleBananaItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.CASSETTE_TAPE:
                await self.__handleCassetteTapeItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.GRENADE:
                await self.__handleGrenadeItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case _:
                raise UnknownChatterItemTypeException(f'Encountered unknown ChatterItemType: \"{action}\"')

    def setEventListener(self, listener: ChatterItemEventListener | None):
        if listener is not None and not isinstance(listener, ChatterItemEventListener):
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
        while True:
            actions: FrozenList[AbsChatterItemAction] = FrozenList()

            try:
                while not self.__actionQueue.empty():
                    action = self.__actionQueue.get_nowait()
                    actions.append(action)
            except queue.Empty as e:
                self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}): {e}', e, traceback.format_exc())

            actions.freeze()

            for index, action in enumerate(actions):
                try:
                    await self.__handleItemAction(action)
                except Exception as e:
                    self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered unknown Exception when looping through actions (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}) ({index=}) ({action=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: FrozenList[AbsChatterItemEvent] = FrozenList()

                try:
                    while not self.__eventQueue.empty():
                        event = self.__eventQueue.get_nowait()
                        events.append(event)
                except queue.Empty as e:
                    self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({events=}): {e}', e, traceback.format_exc())

                events.freeze()

                for index, event in enumerate(events):
                    try:
                        await eventListener.onNewChatterItemEvent(event)
                    except Exception as e:
                        self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({index=}) ({event=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def submitAction(self, action: AbsChatterItemAction):
        if not isinstance(action, AbsChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitEvent(self, event: AbsChatterItemEvent):
        if not isinstance(event, AbsChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('ChatterInventoryItemUseMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
