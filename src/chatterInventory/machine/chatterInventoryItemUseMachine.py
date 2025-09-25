import asyncio
import queue
import random
import traceback
from dataclasses import dataclass
from queue import SimpleQueue
from typing import Final

from frozendict import frozendict
from frozenlist import FrozenList

from .chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..exceptions import CassetteTapeFeatureIsDisabledException, CassetteTapeMessageHasNoTargetException, \
    CassetteTapeTargetIsNotFollowingException, UnknownChatterItemTypeException, \
    UserTwitchAccessTokenIsMissing, VoicemailMessageIsEmptyException, VoicemailTargetIsOriginatingUserException, \
    VoicemailTargetIsStreamerException
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ..models.absChatterItemAction import AbsChatterItemAction
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.events.absChatterItemEvent import AbsChatterItemEvent
from ..models.events.animalPetChatterItemEvent import AnimalPetChatterItemEvent
from ..models.events.cassetteTapeMessageHasNoTargetChatterItemEvent import \
    CassetteTapeMessageHasNoTargetChatterItemEvent
from ..models.events.cassetteTapeTargetIsNotFollowingChatterItemEvent import \
    CassetteTapeTargetIsNotFollowingChatterItemEvent
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.gashaponResultsChatterItemEvent import GashaponResultsChatterItemEvent
from ..models.events.noGashaponResultsChatterItemEvent import NoGashaponResultsChatterItemEvent
from ..models.events.notEnoughInventoryChatterItemEvent import NotEnoughInventoryChatterItemEvent
from ..models.events.tradeChatterItemEvent import TradeChatterItemEvent
from ..models.events.tradeChatterItemTypeDisabledItemEvent import TradeChatterItemTypeDisabledItemEvent
from ..models.events.tradeChatterNotEnoughInventoryItemEvent import TradeChatterNotEnoughInventoryItemEvent
from ..models.events.useAirStrikeChatterItemEvent import UseAirStrikeChatterItemEvent
from ..models.events.useBananaChatterItemEvent import UseBananaChatterItemEvent
from ..models.events.useCassetteTapeChatterItemEvent import UseCassetteTapeChatterItemEvent
from ..models.events.useGrenadeChatterItemEvent import UseGrenadeChatterItemEvent
from ..models.events.useTm36ChatterItemEvent import UseTm36ChatterItemEvent
from ..models.events.voicemailMessageIsEmptyChatterItemEvent import VoicemailMessageIsEmptyChatterItemEvent
from ..models.events.voicemailTargetIsOriginatingUserChatterItemEvent import \
    VoicemailTargetIsOriginatingUserChatterItemEvent
from ..models.events.voicemailTargetIsStreamerChatterItemEvent import VoicemailTargetIsStreamerChatterItemEvent
from ..models.tradeChatterItemAction import TradeChatterItemAction
from ..models.useChatterItemAction import UseChatterItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..useCases.cassetteTapeItemUseCase import CassetteTapeItemUseCase
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ...timeout.models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ...timeout.models.actions.bananaTimeoutAction import BananaTimeoutAction
from ...timeout.models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ...timeout.models.actions.tm36TimeoutAction import Tm36TimeoutAction
from ...timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from ...timeout.models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
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
        cassetteTapeItemUseCase: CassetteTapeItemUseCase,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(cassetteTapeItemUseCase, CassetteTapeItemUseCase):
            raise TypeError(f'cassetteTapeItemUseCase argument is malformed: \"{cassetteTapeItemUseCase}\"')
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
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
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
        self.__cassetteTapeItemUseCase: Final[CassetteTapeItemUseCase] = cassetteTapeItemUseCase
        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__actionQueue: Final[SimpleQueue[AbsChatterItemAction]] = SimpleQueue()
        self.__eventQueue: Final[SimpleQueue[AbsChatterItemEvent]] = SimpleQueue()

        self.__isStarted: bool = False
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

    async def __handleAnimalPetItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getAnimalPetItemDetails()

        updatedInventory: ChatterInventoryData | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryRepository.update(
                itemType = ChatterItemType.ANIMAL_PET,
                changeAmount = -1,
                chatterUserId = action.chatterUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(AnimalPetChatterItemEvent(
            itemDetails = itemDetails,
            updatedInventory = updatedInventory,
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
        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = action.chatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = action.twitchChannelId,
            ),
        )

        try:
            result = await self.__cassetteTapeItemUseCase.invoke(
                action = action,
            )
        except CassetteTapeFeatureIsDisabledException:
            await self.__submitEvent(DisabledFeatureChatterItemEvent(
                originatingAction = action,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            ))
            return
        except CassetteTapeMessageHasNoTargetException:
            await self.__submitEvent(CassetteTapeMessageHasNoTargetChatterItemEvent(
                chatterUserName = chatterUserName,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return
        except CassetteTapeTargetIsNotFollowingException as e:
            await self.__submitEvent(CassetteTapeTargetIsNotFollowingChatterItemEvent(
                chatterUserName = chatterUserName,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                targetUserId = e.targetUserId,
                targetUserName = e.targetUserName,
                originatingAction = action,
            ))
            return
        except UserTwitchAccessTokenIsMissing as e:
            self.__timber.log('ChatterInventoryItemUseMachine', f'No Twitch access token is available for this user ({action=})', e, traceback.format_exc())
            return
        except VoicemailMessageIsEmptyException:
            await self.__submitEvent(VoicemailMessageIsEmptyChatterItemEvent(
                chatterUserName = chatterUserName,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return
        except VoicemailTargetIsOriginatingUserException:
            await self.__submitEvent(VoicemailTargetIsOriginatingUserChatterItemEvent(
                chatterUserName = chatterUserName,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return
        except VoicemailTargetIsStreamerException:
            await self.__submitEvent(VoicemailTargetIsStreamerChatterItemEvent(
                chatterUserName = chatterUserName,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return

        updatedInventory: ChatterInventoryData | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryRepository.update(
                itemType = ChatterItemType.CASSETTE_TAPE,
                changeAmount = -1,
                chatterUserId = action.chatterUserId,
                twitchChannelId = action.twitchChannelId,
            )

        await self.__submitEvent(UseCassetteTapeChatterItemEvent(
            addVoicemailResult = result.addVoicemailResult,
            updatedInventory = updatedInventory,
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            targetUserId = result.targetUserId,
            targetUserName = result.targetUserName,
            originatingAction = action,
        ))

    async def __handleGashaponItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        if action.ignoreInventory:
            # this item type just doesn't make any sense in the context of a disabled/ignored inventory
            await self.__submitEvent(DisabledItemTypeChatterItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return

        itemDetails = await self.__chatterInventorySettings.getGashaponItemDetails()
        awardedItems: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            awardedItems[itemType] = 0

        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        itemsWereAwarded = False

        for _ in range(itemDetails.iterations):
            for itemType in enabledItemTypes:
                if itemType is ChatterItemType.GASHAPON:
                    # for now, let's not allow a gashapon to award another gashapon
                    continue

                randomNumber = random.random()

                if randomNumber < itemDetails.pullRates[itemType]:
                    awardedItems[itemType] += 1
                    itemsWereAwarded = True

        if not itemsWereAwarded:
            await self.__submitEvent(NoGashaponResultsChatterItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
                originatingAction = action,
            ))
            return

        await self.__chatterInventoryRepository.update(
            itemType = ChatterItemType.GASHAPON,
            changeAmount = -1,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        for itemType in enabledItemTypes:
            changeAmount = awardedItems.get(itemType, 0)

            if changeAmount != 0:
                await self.__chatterInventoryRepository.update(
                    itemType = itemType,
                    changeAmount = awardedItems[itemType],
                    chatterUserId = action.chatterUserId,
                    twitchChannelId = action.twitchChannelId,
                )

        updatedInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        await self.__submitEvent(GashaponResultsChatterItemEvent(
            updatedInventory = updatedInventory,
            awardedItems = frozendict(awardedItems),
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            hypeEmote = await self.__trollmojiHelper.getHypeEmoteOrBackup(),
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

        if not await self.__chatterInventorySettings.isEnabled():
            await self.__submitEvent(DisabledFeatureChatterItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))

        elif isinstance(action, TradeChatterItemAction):
            await self.__handleTradeItemAction(
                action = action,
            )

        elif isinstance(action, UseChatterItemAction):
            await self.__handleUseItemAction(
                action = action,
            )

        else:
            raise ValueError(f'Encountered unknown AbsChatterItemAction: \"{action}\"')

    async def __handleTm36ItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getTm36ItemDetails()

        timeoutDuration: AbsTimeoutDuration = RandomLinearTimeoutDuration(
            maximumSeconds = itemDetails.maxDurationSeconds,
            minimumSeconds = itemDetails.minDurationSeconds,
        )

        tokensAndDetails = await self.__fetchTokensAndDetails(
            twitchChannelId = action.twitchChannelId,
        )

        self.__timeoutActionMachine.submitAction(Tm36TimeoutAction(
            timeoutDuration = timeoutDuration,
            ignoreInventory = action.ignoreInventory,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            moderatorTwitchAccessToken = tokensAndDetails.moderatorTwitchAccessToken,
            moderatorUserId = tokensAndDetails.moderatorUserId,
            targetUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
            twitchChatMessageId = action.twitchChatMessageId,
            userTwitchAccessToken = tokensAndDetails.userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = action.user,
        ))

        await self.__submitEvent(UseTm36ChatterItemEvent(
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            itemDetails = itemDetails,
            originatingAction = action,
        ))

    async def __handleTradeItemAction(self, action: TradeChatterItemAction):
        if not isinstance(action, TradeChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if action.itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
            await self.__submitEvent(TradeChatterItemTypeDisabledItemEvent(
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                originatingAction = action,
            ))
            return

        fromChatterUserName = await self.__userIdsRepository.requireUserName(
            userId = action.fromChatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = action.twitchChannelId,
            ),
        )

        toChatterUserName = await self.__userIdsRepository.requireUserName(
            userId = action.toChatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = action.twitchChannelId,
            ),
        )

        fromChatterCurrentInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = action.fromChatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        # There is a lot of room for exploitation without this fairly obtuse line.
        # We really, really don't want to allow for anyone to sneak in trade amounts
        # that cause item duplications, cause people to be ripped off, or for people
        # to end up with negative inventory amounts.
        tradeAmount = int(max(min(action.tradeAmount, fromChatterCurrentInventory[action.itemType]), 0))

        if tradeAmount < 1:
            await self.__submitEvent(TradeChatterNotEnoughInventoryItemEvent(
                tradeAmount = tradeAmount,
                eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
                fromChatterUserName = fromChatterUserName,
                toChatterUserName = toChatterUserName,
                originatingAction = action,
            ))
            return

        toChatterInventory = await self.__chatterInventoryRepository.update(
            itemType = action.itemType,
            changeAmount = tradeAmount,
            chatterUserId = action.toChatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        fromChatterInventory = await self.__chatterInventoryRepository.update(
            itemType = action.itemType,
            changeAmount = tradeAmount * -1,
            chatterUserId = action.fromChatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        await self.__submitEvent(TradeChatterItemEvent(
            fromChatterInventory = fromChatterInventory,
            toChatterInventory = toChatterInventory,
            tradeAmount = tradeAmount,
            eventId = await self.__chatterInventoryIdGenerator.generateEventId(),
            fromChatterUserName = fromChatterUserName,
            toChatterUserName = toChatterUserName,
            originatingAction = action,
        ))

    async def __handleUseItemAction(self, action: UseChatterItemAction):
        if not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if action.itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
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

            case ChatterItemType.ANIMAL_PET:
                await self.__handleAnimalPetItemAction(
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

            case ChatterItemType.GASHAPON:
                await self.__handleGashaponItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.GRENADE:
                await self.__handleGrenadeItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.TM_36:
                await self.__handleTm36ItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case ChatterItemType.VORE:
                await self.__handleVoreItemAction(
                    chatterInventory = chatterInventory,
                    action = action,
                )

            case _:
                raise UnknownChatterItemTypeException(f'Encountered unknown ChatterItemType: \"{action}\"')

    async def __handleVoreItemAction(
        self,
        chatterInventory: ChatterInventoryData | None,
        action: UseChatterItemAction,
    ):
        itemDetails = await self.__chatterInventorySettings.getVoreItemDetails()

        # TODO
        pass

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
