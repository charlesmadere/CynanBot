from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.twitch.exceptions import TwitchAccessTokenMissingException
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface


class TwitchTokensUtils(TwitchTokensUtilsInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository

    async def getAccessTokenOrFallback(self, userName: str) -> Optional[str]:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        if await self.__twitchTokensRepository.hasAccessToken(userName):
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(userName)
            return await self.__twitchTokensRepository.getAccessToken(userName)
        else:
            administratorUserName = await self.__administratorProvider.getAdministratorUserName()
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(administratorUserName)
            return await self.__twitchTokensRepository.getAccessToken(administratorUserName)

    async def requireAccessTokenOrFallback(self, userName: str) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        accessToken = await self.getAccessTokenOrFallback(userName)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Unable to find Twitch access token for \"{userName}\"')

        return accessToken
