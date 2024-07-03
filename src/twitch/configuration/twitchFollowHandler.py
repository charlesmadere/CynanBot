from datetime import datetime

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchFollowHandler import AbsTwitchFollowHandler
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class TwitchFollowHandler(AbsTwitchFollowHandler):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None = twitchFollowingStatusRepository

    async def onNewFollow(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchFollowHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        followedAt = event.followedAt
        followerUserId = event.userId

        await self.__persistFollowingStatus(
            followedAt = followedAt,
            broadcasterUserId = userId,
            followerUserId = followerUserId
        )

    async def __persistFollowingStatus(
        self,
        followedAt: datetime | None,
        broadcasterUserId: str,
        followerUserId: str | None
    ):
        if followedAt is None or not utils.isValidStr(followerUserId):
            return

        twitchFollowingStatusRepository = self.__twitchFollowingStatusRepository

        if twitchFollowingStatusRepository is None:
            return

        await twitchFollowingStatusRepository.persistFollowingStatus(
            followedAt = followedAt,
            twitchChannelId = broadcasterUserId,
            userId = followerUserId
        )
