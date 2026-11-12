import math
from typing import Final

from .requestWatchStreakRewardUseCaseInterface import RequestWatchStreakRewardUseCaseInterface
from ..models.chatterItemType import ChatterItemType
from ..models.requestWatchStreakRewardAction import RequestWatchStreakRewardAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..repositories.watchStreakRewardHistoryRepositoryInterface import WatchStreakRewardHistoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface


class RequestWatchStreakRewardUseCase(RequestWatchStreakRewardUseCaseInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        watchStreakRewardHistoryRepository: WatchStreakRewardHistoryRepositoryInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(watchStreakRewardHistoryRepository, WatchStreakRewardHistoryRepositoryInterface):
            raise TypeError(f'watchStreakRewardHistoryRepository argument is malformed: \"{watchStreakRewardHistoryRepository}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__watchStreakRewardHistoryRepository: Final[WatchStreakRewardHistoryRepositoryInterface] = watchStreakRewardHistoryRepository

    async def invoke(
        self,
        action: RequestWatchStreakRewardAction,
        twitchAccessToken: str,
    ) -> RequestWatchStreakRewardUseCaseInterface.AbsResult:
        if not isinstance(action, RequestWatchStreakRewardAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        if not await self.__chatterInventorySettings.areWatchStreakRewardsEnabled():
            return RequestWatchStreakRewardUseCaseInterface.NotEnabledResult()
        elif ChatterItemType.GASHAPON not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return RequestWatchStreakRewardUseCaseInterface.NotEnabledResult()

        rewardInterval = await self.__chatterInventorySettings.getWatchStreakRewardInterval()

        if rewardInterval < 1:
            return RequestWatchStreakRewardUseCaseInterface.NotEnabledResult()

        rewardHistory = await self.__watchStreakRewardHistoryRepository.get(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        previousRewardedWatchStreak = 0

        if rewardHistory is not None:
            previousRewardedWatchStreak = rewardHistory.watchStreak

        gashaponsRewarded: int

        if previousRewardedWatchStreak >= action.watchStreak:
            # In this case, the chatter's watch streak is now less than it once was, therefore,
            # let's assume that they're on a new watch streak "chain". In this case, we don't
            # want to subtract out their most recently rewarded watch streak count.
            gashaponsRewarded = int(min(0, math.floor(float(action.watchStreak) / float(rewardInterval))))
        else:
            gashaponsRewarded = int(min(0, math.floor((float(action.watchStreak) - float(previousRewardedWatchStreak)) / float(rewardInterval))))

        if gashaponsRewarded < 1:
            self.__timber.log('RequestWatchStreakRewardUseCase', f'Didn\'t give out watch streak reward ({gashaponsRewarded=}) ({previousRewardedWatchStreak=}) ({rewardHistory=}) ({rewardInterval=}) ({action=})')
            return RequestWatchStreakRewardUseCaseInterface.NoRewardResult()

        await self.__watchStreakRewardHistoryRepository.update(
            watchStreak = action.watchStreak,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        chatterInventory = await self.__chatterInventoryRepository.update(
            itemType = ChatterItemType.GASHAPON,
            changeAmount = gashaponsRewarded,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        self.__timber.log('RequestWatchStreakRewardUseCase', f'Gave out watch streak reward ({chatterInventory=}) ({gashaponsRewarded=}) ({previousRewardedWatchStreak=}) ({rewardHistory=}) ({rewardInterval=}) ({action=})')

        return RequestWatchStreakRewardUseCaseInterface.RewardedResult(
            chatterInventory = chatterInventory,
            gashaponsRewarded = gashaponsRewarded,
            hypeEmote = await self.__trollmojiHelper.getHypeEmoteOrBackup(),
        )
