from typing import Optional

from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.twitch.twitchTokensRepository import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository


class AdministratorProvider(AdministratorProviderInterface):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

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
