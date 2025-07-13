from datetime import datetime
from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchFollowHandler import AbsTwitchFollowHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class TwitchFollowHandler(AbsTwitchFollowHandler):

    def __init__(
        self,
        timber: TimberInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface | None] = twitchFollowingStatusRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewFollow(
        self,
        followedAt: datetime,
        followerUserId: str,
        followerUserLogin: str,
        followerUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ):
        if not isinstance(followedAt, datetime):
            raise TypeError(f'followedAt argument is malformed: \"{followedAt}\"')
        elif not utils.isValidStr(followerUserId):
            raise TypeError(f'followerUserId argument is malformed: \"{followerUserId}\"')
        elif not utils.isValidStr(followerUserLogin):
            raise TypeError(f'followerUserLogin argument is malformed: \"{followerUserLogin}\"')
        elif not utils.isValidStr(followerUserName):
            raise TypeError(f'followerUserName argument is malformed: \"{followerUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        await self.__persistFollowingStatus(
            followedAt = followedAt,
            followerUserId = followerUserId,
            twitchChannelId = twitchChannelId,
        )

    async def onNewFollowDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchFollowHandler', f'Received a data bundle that has no event ({user=}) ({dataBundle=})')
            return

        followedAt = event.followedAt
        followerUserId = event.userId
        followerUserLogin = event.userLogin
        followerUserName = event.userName

        if followedAt is None or not utils.isValidStr(followerUserId) or not utils.isValidStr(followerUserLogin) or not utils.isValidStr(followerUserName):
            self.__timber.log('TwitchFollowHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({followedAt=}) ({followerUserId=}) ({followerUserLogin=}) ({followerUserName=})')
            return

        await self.onNewFollow(
            followedAt = followedAt,
            followerUserId = followerUserId,
            followerUserLogin = followerUserLogin,
            followerUserName = followerUserName,
            twitchChannelId = twitchChannelId,
            user = user,
        )

    async def __persistFollowingStatus(
        self,
        followedAt: datetime,
        followerUserId: str,
        twitchChannelId: str,
    ):
        if self.__twitchFollowingStatusRepository is None:
            return

        await self.__twitchFollowingStatusRepository.persistFollowingStatus(
            followedAt = followedAt,
            twitchChannelId = twitchChannelId,
            userId = followerUserId,
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
