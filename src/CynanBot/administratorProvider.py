from typing import Optional

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.twitch.twitchTokensRepository import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class AdministratorProvider(AdministratorProviderInterface):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__administratorUserId: Optional[str] = None

    async def clearCaches(self):
        self.__administratorUserId = None

    async def getAdministratorUserId(self) -> str:
        administratorUserId = self.__administratorUserId

        if administratorUserId is not None:
            return administratorUserId

        userName = await self.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(userName)

        administratorUserId = await self.__userIdsRepository.requireUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        self.__administratorUserId = administratorUserId
        return administratorUserId

    async def getAdministratorUserName(self) -> str:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        return generalSettings.requireAdministrator()
