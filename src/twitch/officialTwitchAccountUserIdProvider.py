from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        twitchAccountUserId: str | None = '12826',
        twitchAnonymousGifterUserId: str | None = '274598607'
    ):
        if twitchAccountUserId is not None and not isinstance(twitchAccountUserId, str):
            raise TypeError(f'twitchAccountUserId argument is malformed: \"{twitchAccountUserId}\"')
        elif twitchAnonymousGifterUserId is not None and not isinstance(twitchAnonymousGifterUserId, str):
            raise TypeError(f'twitchAnonymousGifterUserId argument is malformed: \"{twitchAnonymousGifterUserId}\"')

        self.__twitchAccountUserId: str | None = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: str | None = twitchAnonymousGifterUserId

    async def getTwitchAccountUserId(self) -> str | None:
        return self.__twitchAccountUserId

    async def getTwitchAnonymousGifterUserId(self) -> str | None:
        return self.__twitchAnonymousGifterUserId
