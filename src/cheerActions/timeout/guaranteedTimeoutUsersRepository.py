from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ...aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from ...misc import utils as utils


class GuaranteedTimeoutUsersRepository(GuaranteedTimeoutUsersRepositoryInterface):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider: \"{anivUserIdProvider}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider

        self.__userIds: frozenset[str] | None = None

    async def __createUserIdsSet(self) -> frozenset[str]:
        userIds: set[str] = set()

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()
        if utils.isValidStr(anivUserId):
            userIds.add(anivUserId)

        return frozenset(userIds)

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__userIds

        if userIds is None:
            userIds = await self.__createUserIdsSet()

        return userIds
