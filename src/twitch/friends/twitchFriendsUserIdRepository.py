from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        albeeesUserId: str | None = '61963795',
        charlesUserId: str | None = '74350217',
        eddieUserId: str | None = '22587336',
        hokkaidoubareUserId: str | None = '490529357',
        imytUserId: str | None = '20037000',
        mandooBotUserId: str | None = '761337972',
        oathyBotUserId: str | None = '147389114',
        stashiocatUserId: str | None = '20889981',
        volwrathUserId: str | None = '40463997',
        zanianUserId: str | None = '57704009'
    ):
        if albeeesUserId is not None and not isinstance(albeeesUserId, str):
            raise TypeError(f'albeeesUserId argument is malformed: \"{albeeesUserId}\"')
        elif charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddieUserId argument is malformed: \"{eddieUserId}\"')
        elif hokkaidoubareUserId is not None and not isinstance(hokkaidoubareUserId, str):
            raise TypeError(f'hokkaidoubareUserId argument is malformed: \"{hokkaidoubareUserId}\"')
        elif imytUserId is not None and not isinstance(imytUserId, str):
            raise TypeError(f'imytUserId argument is malformed: \"{imytUserId}\"')
        elif mandooBotUserId is not None and not isinstance(mandooBotUserId, str):
            raise TypeError(f'mandooBotUserId argument is malformed: \"{mandooBotUserId}\"')
        elif oathyBotUserId is not None and not isinstance(oathyBotUserId, str):
            raise TypeError(f'oathyBotUserId argument is malformed: \"{oathyBotUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')
        elif volwrathUserId is not None and not isinstance(volwrathUserId, str):
            raise TypeError(f'volwrathUserId argument is malformed: \"{volwrathUserId}\"')
        elif zanianUserId is not None and not isinstance(zanianUserId, str):
            raise TypeError(f'zanianUserId argument is malformed: \"{zanianUserId}\"')

        self.__albeeesUserId: str | None = albeeesUserId
        self.__charlesUserId: str | None = charlesUserId
        self.__eddieUserId: str | None = eddieUserId
        self.__hokkaidoubareUserId: str | None = hokkaidoubareUserId
        self.__imytUserId: str | None = imytUserId
        self.__mandooBotUserId: str | None = mandooBotUserId
        self.__oathyBotUserId: str | None = oathyBotUserId
        self.__stashiocatUserId: str | None = stashiocatUserId
        self.__volwrathUserId: str | None = volwrathUserId
        self.__zanianUserId: str | None = zanianUserId

    async def getAlbeeesUserId(self) -> str | None:
        return self.__albeeesUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getHokkaidoubareUserId(self) -> str | None:
        return self.__hokkaidoubareUserId

    async def getImytUserId(self) -> str | None:
        return self.__imytUserId

    async def getMandooBotUserId(self) -> str | None:
        return self.__mandooBotUserId

    async def getOathyBotUserId(self) -> str | None:
        return self.__oathyBotUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId

    async def getVolwrathUserId(self) -> str | None:
        return self.__volwrathUserId

    async def getZanianUserId(self) -> str | None:
        return self.__zanianUserId
