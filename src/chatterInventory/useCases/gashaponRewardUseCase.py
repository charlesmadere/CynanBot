from datetime import timedelta
from typing import Final

from .gashaponRewardUseCaseInterface import GashaponRewardUseCaseInterface
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
        chatterInventorySettings: ChatterInventorySettingsInterface,
        gashaponRewardHistoryRepository: GashaponRewardHistoryRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(gashaponRewardHistoryRepository, GashaponRewardHistoryRepositoryInterface):
            raise TypeError(f'gashaponRewardHistoryRepository argument is malformed: \"{gashaponRewardHistoryRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__gashaponRewardHistoryRepository: Final[GashaponRewardHistoryRepositoryInterface] = gashaponRewardHistoryRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository

    async def invoke(
        self,
        action: RequestGashaponRewardAction,
        twitchAccessToken: str,
    ) -> GashaponRewardUseCaseInterface.Result:
        if not isinstance(action, RequestGashaponRewardAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        if not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = action.twitchChannelId,
            userId = action.chatterUserId,
        ):
            return GashaponRewardUseCaseInterface.Result.NOT_FOLLOWING

        elif not await self.__twitchSubscriptionsRepository.isSubscribed(
            chatterUserId = action.chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = action.twitchChannelId,
        ):
            return GashaponRewardUseCaseInterface.Result.NOT_SUBSCRIBED

        rewardHistory = await self.__gashaponRewardHistoryRepository.getHistory(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if rewardHistory is None:
            return GashaponRewardUseCaseInterface.Result.READY

        now = self.__timeZoneRepository.getNow()
        daysBetweenGashaponRewards = await self.__chatterInventorySettings.getDaysBetweenGashaponRewards()
        nextGashaponAvailability = rewardHistory.mostRecentReward + timedelta(days = daysBetweenGashaponRewards)

        if now >= nextGashaponAvailability:
            return GashaponRewardUseCaseInterface.Result.READY
        else:
            return GashaponRewardUseCaseInterface.Result.NOT_READY
