from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..misc import utils as utils
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class GuaranteedTimeoutUsersRepository(GuaranteedTimeoutUsersRepositoryInterface):

    def __init__(
        self,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface
    ):
        if not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository

        self.__userIds: frozenset[str] | None = None

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__userIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()

        acacUserId = await self.__twitchFriendsUserIdRepository.getAcacUserId()
        if utils.isValidStr(acacUserId):
            newUserIds.add(acacUserId)

        albeeesUserId = await self.__twitchFriendsUserIdRepository.getAlbeeesUserId()
        if utils.isValidStr(albeeesUserId):
            newUserIds.add(albeeesUserId)

        aneevUserId = await self.__twitchFriendsUserIdRepository.getAneevUserId()
        if utils.isValidStr(aneevUserId):
            newUserIds.add(aneevUserId)

        anivUserId = await self.__twitchFriendsUserIdRepository.getAnivUserId()
        if utils.isValidStr(anivUserId):
            newUserIds.add(anivUserId)

        frozenUserIds: frozenset[str] = frozenset(newUserIds)
        self.__userIds = frozenUserIds
        return frozenUserIds

    async def isGuaranteed(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        userIds = await self.getUserIds()
        return userId in userIds
