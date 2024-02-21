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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository

    async def getAccessTokenOrFallback(self, twitchChannel: str) -> Optional[str]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if await self.__twitchTokensRepository.hasAccessToken(twitchChannel):
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(twitchChannel)
            return await self.__twitchTokensRepository.getAccessToken(twitchChannel)
        else:
            administratorUserName = await self.__administratorProvider.getAdministratorUserName()
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(administratorUserName)
            return await self.__twitchTokensRepository.getAccessToken(administratorUserName)

    async def requireAccessTokenOrFallback(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessTokenOrFallback(twitchChannel)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Unable to find Twitch access token for \"{twitchChannel}\"')

        return accessToken
