from .seryBotUserIdProviderInterface import SeryBotUserIdProviderInterface


class SeryBotUserIdProvider(SeryBotUserIdProviderInterface):

    def __init__(self, seryBotUserId: str | None = '402337290'):
        if seryBotUserId is not None and not isinstance(seryBotUserId, str):
            raise TypeError(f'seryBotUserId argument is malformed: \"{seryBotUserId}\"')

        self.__seryBotUserId: str | None = seryBotUserId

    async def getSeryBotUserId(self) -> str | None:
        return self.__seryBotUserId
