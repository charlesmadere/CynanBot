from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ...aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface


class GuaranteedTimeoutUsersRepository(GuaranteedTimeoutUsersRepositoryInterface):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider: \"{anivUserIdProvider}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider

    async def getUserIds(self):
        return frozenset()
