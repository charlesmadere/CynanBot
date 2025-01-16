from .puptimeUserIdProviderInterface import PuptimeUserIdProviderInterface


class PuptimeUserIdProvider(PuptimeUserIdProviderInterface):

    def __init__(self, puptimeUserId: str | None = '213177587'):
        if puptimeUserId is not None and not isinstance(puptimeUserId, str):
            raise TypeError(f'puptimeUserId argument is malformed: \"{puptimeUserId}\"')

        self.__puptimeUserId: str | None = puptimeUserId

    async def getPuptimeUserId(self) -> str | None:
        return self.__puptimeUserId
