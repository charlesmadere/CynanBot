from collections import defaultdict
from typing import Final

from frozendict import frozendict

from .gashaponItemUseCaseInterface import GashaponItemUseCaseInterface
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.gashaponTier import GashaponTier
from ..models.useChatterItemAction import UseChatterItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...misc.randomUtilsInterface import RandomUtilsInterface
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier
from ...twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface


class GashaponItemUseCase(GashaponItemUseCaseInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        randomUtils: RandomUtilsInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository

    async def __determineGashaponTier(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> GashaponTier:
        subscriptionStatus = await self.__twitchSubscriptionsRepository.fetchSubscription(
            chatterUserId = action.chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = action.twitchChannelId,
        )

        if subscriptionStatus is None:
            return GashaponTier.TIER_ZERO

        match subscriptionStatus.tier:
            case TwitchSubscriberTier.TIER_TWO: return GashaponTier.TIER_TWO
            case TwitchSubscriberTier.TIER_THREE: return GashaponTier.TIER_THREE
            case _: return GashaponTier.TIER_ONE

    async def __determineInventoryMax(
        self,
        itemType: ChatterItemType,
    ) -> int | None:
        match itemType:
            case ChatterItemType.AIR_STRIKE:
                airStrike = await self.__chatterInventorySettings.getAirStrikeItemDetails()
                return airStrike.inventoryMax

            case ChatterItemType.ANIMAL_PET:
                animalPet = await self.__chatterInventorySettings.getAnimalPetItemDetails()
                return animalPet.inventoryMax

            case ChatterItemType.BANANA:
                banana = await self.__chatterInventorySettings.getBananaItemDetails()
                return banana.inventoryMax

            case ChatterItemType.CASSETTE_TAPE:
                cassetteTape = await self.__chatterInventorySettings.getCassetteTapeItemDetails()
                return cassetteTape.inventoryMax

            case ChatterItemType.CROWD_MIC:
                crowdMic = await self.__chatterInventorySettings.getCrowdMicItemDetails()
                return crowdMic.inventoryMax

            case ChatterItemType.GASHAPON:
                return None

            case ChatterItemType.GRENADE:
                grenade = await self.__chatterInventorySettings.getGrenadeItemDetails()
                return grenade.inventoryMax

            case ChatterItemType.TM_36:
                tm36 = await self.__chatterInventorySettings.getTm36ItemDetails()
                return tm36.inventoryMax

            case ChatterItemType.VORE:
                vore = await self.__chatterInventorySettings.getVoreItemDetails()
                return vore.inventoryMax

    async def invoke(
        self,
        chatterInventory: ChatterInventoryData,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> GashaponItemUseCaseInterface.AbsResult:
        if not isinstance(chatterInventory, ChatterInventoryData):
            raise TypeError(f'chatterInventory argument is malformed: \"{chatterInventory}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()

        if len(enabledItemTypes) == 0:
            return GashaponItemUseCaseInterface.GashaponItemDisabledResult()
        elif len(enabledItemTypes) == 1 and ChatterItemType.GASHAPON in enabledItemTypes:
            # this handles a weird case where the only enabled item type is gashapon, which is a
            # pretty nonsensical scenario but whatever
            return GashaponItemUseCaseInterface.GashaponItemDisabledResult()
        elif ChatterItemType.GASHAPON not in enabledItemTypes:
            return GashaponItemUseCaseInterface.GashaponItemDisabledResult()

        gashaponTier = await self.__determineGashaponTier(
            twitchAccessToken = twitchAccessToken,
            action = action,
        )

        itemDetails = await self.__chatterInventorySettings.getGashaponItemDetails()
        awardedItems: Final[dict[ChatterItemType, int]] = defaultdict(lambda: 0)
        itemsWereAwarded = False

        for itemType, pullRate in itemDetails.pullRates.items():
            if itemType not in enabledItemTypes:
                continue
            elif itemType is ChatterItemType.GASHAPON:
                # for now, let's not allow a gashapon to award another gashapon
                continue

            awardedAmount = 0

            for _ in range(pullRate.iterations):
                randomNumber = self.__randomUtils.float()

                if randomNumber <= pullRate.pullRate:
                    awardedAmount += 1

            awardedAmount = int(min(max(awardedAmount, pullRate.minimumPullAmount), pullRate.maximumPullAmount))

            if not itemsWereAwarded and awardedAmount >= 1:
                itemsWereAwarded = True

            awardedItems[itemType] = awardedAmount

        if not itemsWereAwarded:
            return GashaponItemUseCaseInterface.NoItemsReceivedResult(
                ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
            )

        await self.__chatterInventoryRepository.update(
            itemType = ChatterItemType.GASHAPON,
            changeAmount = -1,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        for itemType in enabledItemTypes:
            changeAmount = awardedItems.get(itemType, 0)

            inventoryMax = await self.__determineInventoryMax(
                itemType = itemType,
            )

            if inventoryMax is not None and changeAmount + chatterInventory[itemType] > inventoryMax:
                changeAmount = int(max(inventoryMax - chatterInventory[itemType], 0))

            if changeAmount != 0:
                await self.__chatterInventoryRepository.update(
                    itemType = itemType,
                    changeAmount = changeAmount,
                    chatterUserId = action.chatterUserId,
                    twitchChannelId = action.twitchChannelId,
                )

        updatedInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        self.__timber.log('GashaponItemUseCase', f'Awarded gashapon items ({awardedItems=}) ({gashaponTier=}) ({action=})')

        return GashaponItemUseCaseInterface.ItemsReceivedResult(
            updatedInventory = updatedInventory,
            awardedItems = frozendict(awardedItems),
            gashaponTier = gashaponTier,
            hypeEmote = await self.__trollmojiHelper.getHypeEmoteOrBackup(),
        )
