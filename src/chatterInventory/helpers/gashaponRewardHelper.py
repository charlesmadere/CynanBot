from datetime import timedelta
from typing import Final

from .chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from .gashaponRewardHelperInterface import GashaponRewardHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.gashaponResults.absGashaponResult import AbsGashaponResult
from ..models.gashaponResults.chatterInventoryDisabledGashaponResult import ChatterInventoryDisabledGashaponResult
from ..models.gashaponResults.gashaponItemDisabledGashaponResult import GashaponItemDisabledGashaponResult
from ..models.gashaponResults.gashaponRewardedGashaponResult import GashaponRewardedGashaponResult
from ..models.gashaponResults.notFollowingGashaponResult import NotFollowingGashaponResult
from ..models.gashaponResults.notReadyGashaponResult import NotReadyGashaponResult
from ..models.gashaponResults.notSubscribedGashaponResult import NotSubscribedGashaponResult
from ..repositories.gashaponRewardHistoryRepositoryInterface import GashaponRewardHistoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface


class GashaponRewardHelper(GashaponRewardHelperInterface):

    def __init__(
        self,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        gashaponRewardHistoryRepository: GashaponRewardHistoryRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
    ):
        if not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(gashaponRewardHistoryRepository, GashaponRewardHistoryRepositoryInterface):
            raise TypeError(f'gashaponRewardHistoryRepository argument is malformed: \"{gashaponRewardHistoryRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__gashaponRewardHistoryRepository: Final[GashaponRewardHistoryRepositoryInterface] = gashaponRewardHistoryRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

    async def checkAndGiveRewardIfAvailable(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AbsGashaponResult:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return ChatterInventoryDisabledGashaponResult()
        elif ChatterItemType.GASHAPON not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return GashaponItemDisabledGashaponResult()

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId,
        ):
            return NotFollowingGashaponResult(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )
        elif not await self.__twitchSubscriptionsRepository.isSubscribed(
            chatterUserId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        ):
            return NotSubscribedGashaponResult(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        rewardHistory = await self.__gashaponRewardHistoryRepository.getHistory(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        if rewardHistory is not None:
            now = self.__timeZoneRepository.getNow()
            daysBetweenGashaponRewards = await self.__chatterInventorySettings.getDaysBetweenGashaponRewards()
            nextGashaponAvailability = rewardHistory.mostRecentReward + timedelta(days = daysBetweenGashaponRewards)

            if now < nextGashaponAvailability:
                return NotReadyGashaponResult(
                    mostRecentGashapon = rewardHistory.mostRecentReward,
                    nextGashaponAvailability = nextGashaponAvailability,
                    daysBetweenGashaponRewards = daysBetweenGashaponRewards,
                    chatterUserId = chatterUserId,
                    twitchChannelId = twitchChannelId,
                )

        giveResult = await self.__chatterInventoryHelper.give(
            itemType = ChatterItemType.GASHAPON,
            giveAmount = 1,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        await self.__gashaponRewardHistoryRepository.noteRewardGiven(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        rewardResult = GashaponRewardedGashaponResult(
            chatterInventory = giveResult.chatterInventory,
            chatterUserId = chatterUserId,
            hypeEmote = await self.__trollmojiHelper.getHypeEmoteOrBackup(),
            twitchChannelId = twitchChannelId,
        )

        self.__timber.log('GashaponRewardHelper', f'Gashapon rewarded ({rewardResult=}) ({giveResult=})')
        return rewardResult
