from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from ..misc import utils as utils
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class GuaranteedTimeoutUsersRepository(GuaranteedTimeoutUsersRepositoryInterface):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository

        self.__userIds: frozenset[str] | None = None

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__userIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()
        if utils.isValidStr(anivUserId):
            newUserIds.add(anivUserId)

        albeeesUserId = await self.__twitchFriendsUserIdRepository.getAlbeeesUserId()
        if utils.isValidStr(albeeesUserId):
            newUserIds.add(albeeesUserId)

        frozenUserIds: frozenset[str] = frozenset(newUserIds)
        self.__userIds = frozenUserIds
        return frozenUserIds

    async def isGuaranteed(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        userIds = await self.getUserIds()
        return userId in userIds
