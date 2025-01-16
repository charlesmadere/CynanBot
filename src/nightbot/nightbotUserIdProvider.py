from .nightbotUserIdProviderInterface import NightbotUserIdProviderInterface


class NightbotUserIdProvider(NightbotUserIdProviderInterface):

    def __init__(self, nightbotUserId: str | None = '19264788'):
        if nightbotUserId is not None and not isinstance(nightbotUserId, str):
            raise TypeError(f'nightbotUserId argument is malformed: \"{nightbotUserId}\"')

        self.__nightbotUserId: str | None = nightbotUserId

    async def getNightbotUserId(self) -> str | None:
        return self.__nightbotUserId
