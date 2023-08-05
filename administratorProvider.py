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
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def getAdministratorUserId(self) -> str:
        userName = await self.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepositoryInterface.getAccessToken(userName)

        return await self.__userIdsRepository.requireUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

    async def getAdministratorUserName(self) -> str:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        return generalSettings.requireAdministrator()
