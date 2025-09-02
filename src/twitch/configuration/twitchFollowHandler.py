from typing import Final

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
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface | None] = twitchFollowingStatusRepository

    async def onNewFollow(self, followData: AbsTwitchFollowHandler.FollowData):
        if not isinstance(followData, AbsTwitchFollowHandler.FollowData):
            raise TypeError(f'followData argument is malformed: \"{followData}\"')

        await self.__persistFollowingStatus(followData)

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

        followData = AbsTwitchFollowHandler.FollowData(
            followedAt = followedAt,
            followerUserId = followerUserId,
            followerUserLogin = followerUserLogin,
            followerUserName = followerUserName,
            twitchChannelId = twitchChannelId,
            user = user,
        )

        await self.onNewFollow(
            followData = followData,
        )

    async def __persistFollowingStatus(self, followData: AbsTwitchFollowHandler.FollowData):
        if not isinstance(followData, AbsTwitchFollowHandler.FollowData):
            raise TypeError(f'followData argument is malformed: \"{followData}\"')

        if self.__twitchFollowingStatusRepository is None:
            return

        await self.__twitchFollowingStatusRepository.persistFollowingStatus(
            followedAt = followData.followedAt,
            twitchChannelId = followData.twitchChannelId,
            userId = followData.followerUserId,
        )
