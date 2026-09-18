from typing import Final

from .administratorProviderInterface import AdministratorProviderInterface
from .generalSettingsRepository import GeneralSettingsRepository
from ..twitch.userIds.twitchUserIdsRepositoryInterface import TwitchUserIdsRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AdministratorProvider(AdministratorProviderInterface):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        twitchUserIdsRepository: TwitchUserIdsRepositoryInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(twitchUserIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'twitchUserIdsRepository argument is malformed: \"{twitchUserIdsRepository}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__twitchUserIdsRepository: Final[TwitchUserIdsRepositoryInterface] = twitchUserIdsRepository

        self.__administratorUserId: str | None = None

    async def clearCaches(self):
        self.__administratorUserId = None

    async def getAdministratorUserId(self) -> str:
        administratorUserId = self.__administratorUserId

        if administratorUserId is not None:
            return administratorUserId

        userLoginOrName = await self.getAdministratorUserName()

        administratorUserId = await self.__twitchUserIdsRepository.requireIdByLoginOrName(
            userLoginOrName = userLoginOrName,
        )

        self.__administratorUserId = administratorUserId
        return administratorUserId

    async def getAdministratorUserName(self) -> str:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        return generalSettings.requireAdministrator()
