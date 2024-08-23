from .tangiaBotUserIdProviderInterface import TangiaBotUserIdProviderInterface


class TangiaBotUserIdProvider(TangiaBotUserIdProviderInterface):

    def __init__(self, tangiaBotUserId: str | None = '853402143'):
        if tangiaBotUserId is not None and not isinstance(tangiaBotUserId, str):
            raise TypeError(f'tangiaBotUserId argument is malformed: \"{tangiaBotUserId}\"')

        self.__tangiaBotUserId: str | None = tangiaBotUserId

    async def getTangiaBotUserId(self) -> str | None:
        return self.__tangiaBotUserId
