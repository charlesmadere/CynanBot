from typing import Final

from .exceptions import FailedToFindTwitchChannelInformationException
from .twitchChannelInformationHelperInterface import TwitchChannelInformationHelperInterface
from ..api.models.twitchChannelInformation import TwitchChannelInformation
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchChannelInformationHelper(TwitchChannelInformationHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

    async def __fetchChannelInformation(
        self,
        twitchChannelId: str,
    ) -> TwitchChannelInformation:
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        response = await self.__twitchApiService.fetchChannelInformation(
            broadcasterId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        for channelInformation in response.data:
            if channelInformation.broadcasterId == twitchChannelId:
                return channelInformation

        raise FailedToFindTwitchChannelInformationException(f'Failed to find corresponding channel information ({twitchChannelId=}) ({response=})')

    async def getGame(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        channelInformation = await self.__fetchChannelInformation(
            twitchChannelId = twitchChannelId,
        )

        return channelInformation.gameName

    async def getTitle(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        channelInformation = await self.__fetchChannelInformation(
            twitchChannelId = twitchChannelId,
        )

        return channelInformation.title

    async def setGame(
        self,
        game: str,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(game):
            raise TypeError(f'game argument is malformed: \"{game}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        raise RuntimeError()

    async def setTitle(
        self,
        title: str,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        raise RuntimeError()
