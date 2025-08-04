import traceback
from typing import Final

from frozendict import frozendict

from .whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..models.whichAnivUser import WhichAnivUser
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class WhichAnivUserHelper(WhichAnivUserHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def getAllAnivUserIds(self) -> frozendict[WhichAnivUser, str | None]:
        acacUserId = await self.__twitchFriendsUserIdRepository.getAcacUserId()
        aneevUserId = await self.__twitchFriendsUserIdRepository.getAneevUserId()
        anivUserId = await self.__twitchFriendsUserIdRepository.getAnivUserId()

        return frozendict({
            WhichAnivUser.ACAC: acacUserId,
            WhichAnivUser.ANEEV: aneevUserId,
            WhichAnivUser.ANIV: anivUserId,
        })

    async def getAnivUser(
        self,
        twitchChannelId: str,
        whichAnivUser: WhichAnivUser | None,
    ) -> WhichAnivUserHelperInterface.Result | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif whichAnivUser is not None and not isinstance(whichAnivUser, WhichAnivUser):
            raise TypeError(f'whichAnivUser argument is malformed: \"{whichAnivUser}\"')

        if whichAnivUser is None:
            return None

        allAnivUserIds = await self.getAllAnivUserIds()
        anivUserId = allAnivUserIds.get(whichAnivUser, None)

        if not utils.isValidStr(anivUserId):
            self.__timber.log('WhichAnivUserHelper', f'No user ID is available for this aniv user ({whichAnivUser=}) ({anivUserId=})')
            return None

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            anivUserName = await self.__userIdsRepository.fetchUserName(
                userId = anivUserId,
                twitchAccessToken = twitchAccessToken,
            )
        except Exception as e:
            self.__timber.log('WhichAnivUserHelper', f'Failed to fetch username for this aniv user ({whichAnivUser=}) ({anivUserId=}): {e}', e, traceback.format_exc())
            return None

        return WhichAnivUserHelperInterface.Result(
            userId = anivUserId,
            userName = anivUserName,
            whichAnivUser = whichAnivUser,
        )
