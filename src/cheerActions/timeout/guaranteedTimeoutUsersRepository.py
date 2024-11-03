from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ...aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from ...misc import utils as utils
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


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

        self.__cachedGuaranteedUserIds: frozenset[str] | None = None

    async def __getGuaranteedUserIds(self) -> frozenset[str]:
        cachedGuaranteedUserIds = self.__cachedGuaranteedUserIds

        if cachedGuaranteedUserIds is not None:
            return cachedGuaranteedUserIds

        guaranteedUserIds: set[str] = set()

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()
        if utils.isValidStr(anivUserId):
            guaranteedUserIds.add(anivUserId)

        albeeesUserId = await self.__twitchFriendsUserIdRepository.getAlbeeesUserId()
        if utils.isValidStr(albeeesUserId):
            guaranteedUserIds.add(albeeesUserId)

        cachedGuaranteedUserIds = frozenset(guaranteedUserIds)
        self.__cachedGuaranteedUserIds = cachedGuaranteedUserIds
        return cachedGuaranteedUserIds

    async def isGuaranteed(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        guaranteedUserIds = await self.__getGuaranteedUserIds()
        return userId in guaranteedUserIds
