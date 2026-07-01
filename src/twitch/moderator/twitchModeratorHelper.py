import traceback
from typing import Final

from .twitchModeratorHelperInterface import TwitchModeratorHelperInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchModeratorHelper(TwitchModeratorHelperInterface):

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

    async def clearCaches(self):
        # intentionally empty for now
        pass

    async def isModerator(self, request: TwitchModeratorHelperInterface.AbsRequest) -> bool:
        if not isinstance(request, TwitchModeratorHelperInterface.AbsRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        twitchAccessToken: str | None

        if isinstance(request, TwitchModeratorHelperInterface.RequestWithAccessToken):
            twitchAccessToken = request.twitchAccessToken

        elif isinstance(request, TwitchModeratorHelperInterface.Request):
            twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                twitchChannelId = request.getTwitchChannelId(),
            )

            if not utils.isValidStr(twitchAccessToken):
                self.__timber.log('TwitchModeratorHelper', f'No Twitch access token is available to check chatter moderator status ({request=})')
                return False

        else:
            raise ValueError(f'request argument is unknown TwitchModeratorHelperInterface.AbsRequest type: \"{request}\"')

        try:
            response = await self.__twitchApiService.fetchModerator(
                broadcasterId = request.getTwitchChannelId(),
                twitchAccessToken = twitchAccessToken,
                userId = request.getChatterUserId(),
            )
        except Exception as e:
            self.__timber.log('TwitchModeratorHelper', f'Failed to check moderator status ({request=})', e, traceback.format_exc())
            return False

        for moderatorUser in response.data:
            if moderatorUser.userId == request.getChatterUserId():
                return True

        return False
