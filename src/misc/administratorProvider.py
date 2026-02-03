from typing import Final

from .administratorProviderInterface import AdministratorProviderInterface
from .generalSettingsRepository import GeneralSettingsRepository
from ..twitch.tokens.twitchTokensRepository import TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AdministratorProvider(AdministratorProviderInterface):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__administratorUserId: str | None = None

    async def clearCaches(self):
        self.__administratorUserId = None

    async def getAdministratorUserId(self) -> str:
        administratorUserId = self.__administratorUserId

        if administratorUserId is not None:
            return administratorUserId

        userName = await self.getAdministratorUserName()

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = userName,
        )

        administratorUserId = await self.__userIdsRepository.requireUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken,
        )

        self.__administratorUserId = administratorUserId
        return administratorUserId

    async def getAdministratorUserName(self) -> str:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        return generalSettings.requireAdministrator()
