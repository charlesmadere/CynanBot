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
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository

    async def getAccessTokenOrFallback(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if await self.__twitchTokensRepository.hasAccessToken(twitchChannel):
            return await self.__twitchTokensRepository.getAccessToken(twitchChannel)
        else:
            administratorUserId = await self.__administratorProvider.getAdministratorUserId()
            return await self.__twitchTokensRepository.getAccessTokenById(administratorUserId)

    async def getAccessTokenByIdOrFallback(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if await self.__twitchTokensRepository.hasAccessTokenById(twitchChannelId):
            return await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)
        else:
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
