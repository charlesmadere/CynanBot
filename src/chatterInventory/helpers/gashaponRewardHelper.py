from datetime import datetime, timedelta
from typing import Final

from .gashaponRewardHelperInterface import GashaponRewardHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.giveGashaponRewardResult import GiveGashaponRewardResult
from ..repositories.gashaponRewardHistoryRepositoryInterface import GashaponRewardHistoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface


class GashaponRewardHelper(GashaponRewardHelperInterface):

    def __init__(
        self,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        gashaponRewardHistoryRepository: GashaponRewardHistoryRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(gashaponRewardHistoryRepository, GashaponRewardHistoryRepositoryInterface):
            raise TypeError(f'gashaponRewardHistoryRepository argument is malformed: \"{gashaponRewardHistoryRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__gashaponRewardHistoryRepository: Final[GashaponRewardHistoryRepositoryInterface] = gashaponRewardHistoryRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

    async def checkAndGiveRewardIfAvailable(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> GiveGashaponRewardResult:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return GiveGashaponRewardResult.CHATTER_INVENTORY_DISABLED
        elif ChatterItemType.GASHAPON not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return GiveGashaponRewardResult.GASHAPON_ITEM_DISABLED

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId,
        ):
            return GiveGashaponRewardResult.NOT_FOLLOWING
        elif not await self.__twitchSubscriptionsRepository.isChatterSubscribed(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId,
        ):
            return GiveGashaponRewardResult.NOT_SUBSCRIBED
        elif await self.__hasRecentlyReceivedGashaponReward(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        ):
            return GiveGashaponRewardResult.NOT_READY

        # TODO
        return GiveGashaponRewardResult.GASHAPON_ITEM_DISABLED

    async def __hasRecentlyReceivedGashaponReward(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        rewardHistory = await self.__gashaponRewardHistoryRepository.getHistory(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        if rewardHistory is None:
            return False

        daysBetweenGashaponRewards = timedelta(
            days = await self.__chatterInventorySettings.getDaysBetweenGashaponRewards(),
        )

        now = datetime.now(self.__timeZoneRepository.getDefault())

        return rewardHistory.mostRecentReward + daysBetweenGashaponRewards <= now
