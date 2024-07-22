from .funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface


class FuntoonUserIdProvider(FuntoonUserIdProviderInterface):

    def __init__(self, funtoonUserId: str | None = '477393386'):
        if funtoonUserId is not None and not isinstance(funtoonUserId, str):
            raise TypeError(f'funtoonUserId argument is malformed: \"{funtoonUserId}\"')

        self.__funtoonUserId: str | None = funtoonUserId

    async def getFuntoonUserId(self) -> str | None:
        return self.__funtoonUserId
