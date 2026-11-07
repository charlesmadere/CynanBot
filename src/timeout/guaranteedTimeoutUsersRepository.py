from typing import Final

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..aniv.repositories.anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class GuaranteedTimeoutUsersRepository(GuaranteedTimeoutUsersRepositoryInterface):

    def __init__(
        self,
        anivUserIdsRepository: AnivUserIdsRepositoryInterface,
        timber: TimberInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(anivUserIdsRepository, AnivUserIdsRepositoryInterface):
            raise TypeError(f'anivUserIdsRepository argument is malformed: \"{anivUserIdsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__anivUserIdsRepository: Final[AnivUserIdsRepositoryInterface] = anivUserIdsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

        self.__userIds: frozenset[str] | None = None

    async def clearCaches(self):
        self.__userIds = None
        self.__timber.log('GuaranteedTimeoutUsersRepository', 'Caches cleared')

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__userIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()

        acacUserId = await self.__anivUserIdsRepository.getAcacUserId()
        if utils.isValidStr(acacUserId):
            newUserIds.add(acacUserId)

        albeeevUserId = await self.__anivUserIdsRepository.getAlbeeevUserId()
        if utils.isValidStr(albeeevUserId):
            newUserIds.add(albeeevUserId)

        aneevUserId = await self.__anivUserIdsRepository.getAneevUserId()
        if utils.isValidStr(aneevUserId):
            newUserIds.add(aneevUserId)

        anivUserId = await self.__anivUserIdsRepository.getAnivUserId()
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
