from typing import Final

from .refreshCrowdMicrophonesUseCaseInterface import RefreshCrowdMicrophonesUseCaseInterface
from ..helpers.crowdMicrophoneHelperInterface import CrowdMicrophoneHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...timber.timberInterface import TimberInterface


class RefreshCrowdMicrophonesUseCase(RefreshCrowdMicrophonesUseCaseInterface):

    def __init__(
        self,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        crowdMicrophoneHelper: CrowdMicrophoneHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(crowdMicrophoneHelper, CrowdMicrophoneHelperInterface):
            raise TypeError(f'crowdMicrophoneHelper argument is malformed: \"{crowdMicrophoneHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__crowdMicrophoneHelper: Final[CrowdMicrophoneHelperInterface] = crowdMicrophoneHelper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def invoke(self) -> RefreshCrowdMicrophonesUseCaseInterface.Result:
        if ChatterItemType.CROWD_MIC not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return RefreshCrowdMicrophonesUseCaseInterface.Result(
                deadMicrophones = frozenset(),
            )

        deadMicrophones = await self.__crowdMicrophoneHelper.getAllDeadMicrophones()

        if len(deadMicrophones) >= 1:
            for deadMicrophone in deadMicrophones:
                await self.__crowdMicrophoneHelper.stopMicrophone(
                    twitchChannelId = deadMicrophone.twitchChannelId,
                )

            self.__timber.log('RefreshCrowdMicrophonesUseCase', f'Finished removing dead crowd microphones ({deadMicrophones=})')

        return RefreshCrowdMicrophonesUseCaseInterface.Result(
            deadMicrophones = deadMicrophones,
        )
