from .anivUserIdProviderInterface import AnivUserIdProviderInterface


class AnivUserIdProvider(AnivUserIdProviderInterface):

    def __init__(
        self,
        aneevUserId: str | None = '1284413302',
        anivUserId: str | None = '749050409'
    ):
        if aneevUserId is not None and not isinstance(aneevUserId, str):
            raise TypeError(f'aneevUserId argument is malformed: \"{aneevUserId}\"')
        elif anivUserId is not None and not isinstance(anivUserId, str):
            raise TypeError(f'anivUserId argument is malformed: \"{anivUserId}\"')

        self.__aneevUserId: str | None = aneevUserId
        self.__anivUserId: str | None = anivUserId

    async def getAneevUserId(self) -> str | None:
        return self.__aneevUserId

    async def getAnivUserId(self) -> str | None:
        # this is stupid but oh well, aniv was banned and so now we are using "a_n_e_e_v" instead
        return await self.getAneevUserId()
