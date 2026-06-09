from typing import Final

from .exceptions import (FailedToFindTwitchChannelInformationException,
                         FailedToFindTwitchGameException,
                         FailedToSetTwitchChannelGameException,
                         FailedToSetTwitchChannelTitleException)
from .twitchChannelInformationHelperInterface import TwitchChannelInformationHelperInterface
from ..api.models.twitchChannelInformation import TwitchChannelInformation
from ..api.models.twitchGame import TwitchGame
from ..api.models.twitchModifyChannelInformationRequest import TwitchModifyChannelInformationRequest
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
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchChannelInformation:
        response = await self.__twitchApiService.fetchChannelInformation(
            broadcasterId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        for channelInformation in response.data:
            if channelInformation.broadcasterId == twitchChannelId:
                return channelInformation

        raise FailedToFindTwitchChannelInformationException(f'Failed to find corresponding channel information ({twitchChannelId=}) ({response=})')

    async def __fetchGame(
        self,
        gameName: str,
        twitchAccessToken: str,
    ) -> TwitchGame:
        response = await self.__twitchApiService.fetchGames(
            gameName = gameName,
            twitchAccessToken = twitchAccessToken,
        )

        for game in response.data:
            if game.gameName.casefold() == gameName.casefold():
                return game

        raise FailedToFindTwitchGameException(f'Failed to find corresponding Twitch game ({gameName=}) ({response=})')

    async def getGame(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        channelInformation = await self.__fetchChannelInformation(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        return channelInformation.gameName

    async def getTitle(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        channelInformation = await self.__fetchChannelInformation(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        return channelInformation.title

    async def setGame(
        self,
        gameName: str,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(gameName):
            raise TypeError(f'gameName argument is malformed: \"{gameName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        game = await self.__fetchGame(
            gameName = gameName,
            twitchAccessToken = twitchAccessToken,
        )

        await self.__twitchApiService.modifyChannelInformation(
            twitchAccessToken = twitchAccessToken,
            modifyChannelInformationRequest = TwitchModifyChannelInformationRequest(
                gameId = game.gameId,
                title = None,
                twitchChannelId = twitchChannelId,
            )
        )

        channelInformation = await self.__fetchChannelInformation(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(channelInformation.gameName):
            raise FailedToSetTwitchChannelGameException(f'Failed to set Twitch game ({channelInformation=}) ({gameName=})')

        return channelInformation.gameName

    async def setTitle(
        self,
        title: str,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        await self.__twitchApiService.modifyChannelInformation(
            twitchAccessToken = twitchAccessToken,
            modifyChannelInformationRequest = TwitchModifyChannelInformationRequest(
                gameId = None,
                title = title,
                twitchChannelId = twitchChannelId,
            )
        )

        channelInformation = await self.__fetchChannelInformation(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(channelInformation.title):
            raise FailedToSetTwitchChannelTitleException(f'Failed to set Twitch channel title ({channelInformation=}) ({title=})')

        return channelInformation.title
