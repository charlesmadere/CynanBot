from typing import Final

from .requestWatchStreakRewardUseCaseInterface import RequestWatchStreakRewardUseCaseInterface
from ..models.chatterItemType import ChatterItemType
from ..models.requestWatchStreakRewardAction import RequestWatchStreakRewardAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..repositories.watchStreakRewardHistoryRepositoryInterface import WatchStreakRewardHistoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class RequestWatchStreakRewardUseCase(RequestWatchStreakRewardUseCaseInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        watchStreakRewardHistoryRepository: WatchStreakRewardHistoryRepositoryInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(watchStreakRewardHistoryRepository, WatchStreakRewardHistoryRepositoryInterface):
            raise TypeError(f'watchStreakRewardHistoryRepository argument is malformed: \"{watchStreakRewardHistoryRepository}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
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

        return RequestWatchStreakRewardUseCaseInterface.NoRewardResult()
