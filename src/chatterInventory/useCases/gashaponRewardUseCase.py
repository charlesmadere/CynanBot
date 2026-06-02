from datetime import timedelta
from typing import Final

from .gashaponRewardUseCaseInterface import GashaponRewardUseCaseInterface
from ..helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.requestGashaponRewardAction import RequestGashaponRewardAction
from ..repositories.gashaponRewardHistoryRepositoryInterface import \
    GashaponRewardHistoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface


class GashaponRewardUseCase(GashaponRewardUseCaseInterface):

    def __init__(
        self,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        gashaponRewardHistoryRepository: GashaponRewardHistoryRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
    ):
        if not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(gashaponRewardHistoryRepository, GashaponRewardHistoryRepositoryInterface):
            raise TypeError(f'gashaponRewardHistoryRepository argument is malformed: \"{gashaponRewardHistoryRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')

        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__gashaponRewardHistoryRepository: Final[GashaponRewardHistoryRepositoryInterface] = gashaponRewardHistoryRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository

    async def invoke(
        self,
        action: RequestGashaponRewardAction,
        twitchAccessToken: str,
    ) -> GashaponRewardUseCaseInterface.AbsResult:
        if not isinstance(action, RequestGashaponRewardAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        if not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userId = action.chatterUserId,
        ):
            return GashaponRewardUseCaseInterface.NotFollowingResult()

        elif not await self.__twitchSubscriptionsRepository.isSubscribed(
            chatterUserId = action.chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = action.twitchChannelId,
        ):
            return GashaponRewardUseCaseInterface.NotSubscribedResult()

        rewardHistory = await self.__gashaponRewardHistoryRepository.getHistory(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if rewardHistory is not None:
            now = self.__timeZoneRepository.getNow()
            daysBetweenGashaponRewards = await self.__chatterInventorySettings.getDaysBetweenGashaponRewards()
            nextGashaponAvailability = rewardHistory.mostRecentReward + timedelta(days = daysBetweenGashaponRewards)

            if now < nextGashaponAvailability:
                return GashaponRewardUseCaseInterface.NotReadyResult(
                    nextGashaponAvailability = nextGashaponAvailability,
                )

        giveResult = await self.__chatterInventoryHelper.give(
            itemType = ChatterItemType.GASHAPON,
            giveAmount = 1,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        await self.__gashaponRewardHistoryRepository.noteRewardGiven(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        return GashaponRewardUseCaseInterface.RewardedResult(
            chatterInventory = giveResult.chatterInventory,
        )
