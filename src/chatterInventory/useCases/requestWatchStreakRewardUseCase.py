from typing import Final

from .requestWatchStreakRewardUseCaseInterface import RequestWatchStreakRewardUseCaseInterface
from ..models.chatterItemType import ChatterItemType
from ..models.requestWatchStreakRewardAction import RequestWatchStreakRewardAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...timber.timberInterface import TimberInterface


class RequestWatchStreakRewardUseCase(RequestWatchStreakRewardUseCaseInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber

    async def invoke(
        self,
        action: RequestWatchStreakRewardAction,
    ) -> RequestWatchStreakRewardUseCaseInterface.AbsResult:
        if not isinstance(action, RequestWatchStreakRewardAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__chatterInventorySettings.areWatchStreakRewardsEnabled():
            return RequestWatchStreakRewardUseCaseInterface.NotEnabledResult()
        elif ChatterItemType.GASHAPON not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return RequestWatchStreakRewardUseCaseInterface.NotEnabledResult()

        return RequestWatchStreakRewardUseCaseInterface.NoRewardResult()
