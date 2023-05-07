from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.twitch.twitchTokensRepository import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from generalSettingsRepository import GeneralSettingsRepository


class AdministratorProvider(AdministratorProviderInterface):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__userIdsRepository: UserIdsRepository = userIdsRepository

    async def getAdministratorUserId(self) -> str:
        userName = await self.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepositoryInterface.getAccessToken(userName)

        return await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

    async def getAdministratorUserName(self) -> str:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        return generalSettings.requireAdministrator()
