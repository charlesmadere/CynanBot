from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        albeeesUserId: str | None = '61963795',
        bastionBlueUserId: str | None = '134639294',
        charlesUserId: str | None = '74350217',
        eddieUserId: str | None = '22587336',
        hokkaidoubareUserId: str | None = '490529357',
        imytUserId: str | None = '20037000',
        jrpUserId: str | None = '47768842',
        lucentUserId: str | None = '30992900',
        mandooBotUserId: str | None = '761337972',
        merttUserId: str | None = '76798688',
        oathyBotUserId: str | None = '147389114',
        stashiocatUserId: str | None = '20889981',
        volwrathUserId: str | None = '40463997',
        zanianUserId: str | None = '57704009'
    ):
        if albeeesUserId is not None and not isinstance(albeeesUserId, str):
            raise TypeError(f'albeeesUserId argument is malformed: \"{albeeesUserId}\"')
        elif bastionBlueUserId is not None and not isinstance(bastionBlueUserId, str):
            raise TypeError(f'bastionBlueUserId argument is malformed: \"{bastionBlueUserId}\"')
        elif charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddieUserId argument is malformed: \"{eddieUserId}\"')
        elif hokkaidoubareUserId is not None and not isinstance(hokkaidoubareUserId, str):
            raise TypeError(f'hokkaidoubareUserId argument is malformed: \"{hokkaidoubareUserId}\"')
        elif imytUserId is not None and not isinstance(imytUserId, str):
            raise TypeError(f'imytUserId argument is malformed: \"{imytUserId}\"')
        elif jrpUserId is not None and not isinstance(jrpUserId, str):
            raise TypeError(f'jrpUserId argument is malformed: \"{jrpUserId}\"')
        elif lucentUserId is not None and not isinstance(lucentUserId, str):
            raise TypeError(f'lucentUserId argument is malformed: \"{lucentUserId}\"')
        elif mandooBotUserId is not None and not isinstance(mandooBotUserId, str):
            raise TypeError(f'mandooBotUserId argument is malformed: \"{mandooBotUserId}\"')
        elif merttUserId is not None and not isinstance(merttUserId, str):
            raise TypeError(f'merttUserId argument is malformed: \"{merttUserId}\"')
        elif oathyBotUserId is not None and not isinstance(oathyBotUserId, str):
            raise TypeError(f'oathyBotUserId argument is malformed: \"{oathyBotUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')
        elif volwrathUserId is not None and not isinstance(volwrathUserId, str):
            raise TypeError(f'volwrathUserId argument is malformed: \"{volwrathUserId}\"')
        elif zanianUserId is not None and not isinstance(zanianUserId, str):
            raise TypeError(f'zanianUserId argument is malformed: \"{zanianUserId}\"')

        self.__albeeesUserId: str | None = albeeesUserId
        self.__bastionBlueUserId: str | None = bastionBlueUserId
        self.__charlesUserId: str | None = charlesUserId
        self.__eddieUserId: str | None = eddieUserId
        self.__hokkaidoubareUserId: str | None = hokkaidoubareUserId
        self.__imytUserId: str | None = imytUserId
        self.__jrpUserId: str | None = jrpUserId
        self.__lucentUserId: str | None = lucentUserId
        self.__mandooBotUserId: str | None = mandooBotUserId
        self.__merttUserId: str | None = merttUserId
        self.__oathyBotUserId: str | None = oathyBotUserId
        self.__stashiocatUserId: str | None = stashiocatUserId
        self.__volwrathUserId: str | None = volwrathUserId
        self.__zanianUserId: str | None = zanianUserId

    async def getAlbeeesUserId(self) -> str | None:
        return self.__albeeesUserId

    async def getBastionBlueUserId(self) -> str | None:
        return self.__bastionBlueUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getHokkaidoubareUserId(self) -> str | None:
        return self.__hokkaidoubareUserId

    async def getImytUserId(self) -> str | None:
        return self.__imytUserId

    async def getJrpUserId(self) -> str | None:
        return self.__jrpUserId

    async def getLucentUserId(self) -> str | None:
        return self.__lucentUserId

    async def getMandooBotUserId(self) -> str | None:
        return self.__mandooBotUserId

    async def getMerttUserId(self) -> str | None:
        return self.__merttUserId

    async def getOathyBotUserId(self) -> str | None:
        return self.__oathyBotUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId

    async def getVolwrathUserId(self) -> str | None:
        return self.__volwrathUserId

    async def getZanianUserId(self) -> str | None:
        return self.__zanianUserId
