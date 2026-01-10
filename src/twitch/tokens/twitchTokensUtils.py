from typing import Final

from .twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..exceptions import TwitchAccessTokenMissingException
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface


class TwitchTokensUtils(TwitchTokensUtilsInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

    async def getAccessTokenOrFallback(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchChannel)

        if utils.isValidStr(twitchChannelAccessToken):
            return twitchChannelAccessToken

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()
        return await self.__twitchTokensRepository.getAccessTokenById(administratorUserId)

    async def getAccessTokenByIdOrFallback(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchChannelAccessToken =  await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)

        if utils.isValidStr(twitchChannelAccessToken):
            return twitchChannelAccessToken

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()
        return await self.__twitchTokensRepository.getAccessTokenById(administratorUserId)

    async def requireAccessTokenOrFallback(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessTokenOrFallback(twitchChannel)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Unable to find Twitch access token for \"{twitchChannel}\"')

        return accessToken

    async def requireAccessTokenByIdOrFallback(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        accessToken = await self.getAccessTokenByIdOrFallback(twitchChannelId)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Unable to find Twitch access token for \"{twitchChannelId}\"')

        return accessToken
