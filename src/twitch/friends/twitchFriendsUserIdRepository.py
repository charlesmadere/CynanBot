from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        albeeesUserId: str | None = '61963795',
        charlesUserId: str | None = '74350217',
        eddieUserId: str | None = '22587336',
        imytUserId: str | None = '20037000',
        mandooBotUserId: str | None = '761337972',
        oathyBotUserId: str | None = '147389114',
        stashiocatUserId: str | None = '20889981'
    ):
        if albeeesUserId is not None and not isinstance(albeeesUserId, str):
            raise TypeError(f'albeeesUserId argument is malformed: \"{albeeesUserId}\"')
        elif charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddieUserId argument is malformed: \"{eddieUserId}\"')
        elif imytUserId is not None and not isinstance(imytUserId, str):
            raise TypeError(f'imytUserId argument is malformed: \"{imytUserId}\"')
        elif mandooBotUserId is not None and not isinstance(mandooBotUserId, str):
            raise TypeError(f'mandooBotUserId argument is malformed: \"{mandooBotUserId}\"')
        elif oathyBotUserId is not None and not isinstance(oathyBotUserId, str):
            raise TypeError(f'oathyBotUserId argument is malformed: \"{oathyBotUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')

        self.__albeeesUserId: str | None = albeeesUserId
        self.__charlesUserId: str | None = charlesUserId
        self.__eddieUserId: str | None = eddieUserId
        self.__imytUserId: str | None = imytUserId
        self.__mandooBotUserId: str | None = mandooBotUserId
        self.__oathyBotUserId: str | None = oathyBotUserId
        self.__stashiocatUserId: str | None = stashiocatUserId

    async def getAlbeeesUserId(self) -> str | None:
        return self.__albeeesUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getImytUserId(self) -> str | None:
        return self.__imytUserId

    async def getMandooBotUserId(self) -> str | None:
        return self.__mandooBotUserId

    async def getOathyBotUserId(self) -> str | None:
        return self.__oathyBotUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId
