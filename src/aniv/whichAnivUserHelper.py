from .whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..users.aniv.whichAnivUser import WhichAnivUser


class WhichAnivUserHelper(WhichAnivUserHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository

    async def getAnivUser(self, whichAnivUser: WhichAnivUser | None) -> WhichAnivUserHelperInterface.Result | None:
        if whichAnivUser is not None and not isinstance(whichAnivUser, WhichAnivUser):
            raise TypeError(f'whichAnivUser argument is malformed: \"{whichAnivUser}\"')

        if whichAnivUser is None:
            return None

        anivUserId: str | None = None

        match whichAnivUser:
            case WhichAnivUser.ACAC:
                anivUserId = await self.__twitchFriendsUserIdRepository.getAcacUserId()

            case WhichAnivUser.ANEEV:
                anivUserId = await self.__twitchFriendsUserIdRepository.getAneevUserId()

            case WhichAnivUser.ANIV:
                anivUserId = await self.__twitchFriendsUserIdRepository.getAnivUserId()

            case _:
                self.__timber.log('WhichAnivUserHelper', f'No aniv user ID is available for this aniv user ({whichAnivUser=})')

        if not utils.isValidStr(anivUserId):
            return None

        return WhichAnivUserHelperInterface.Result(
            userId = anivUserId,
            whichAnivUser = whichAnivUser
        )
