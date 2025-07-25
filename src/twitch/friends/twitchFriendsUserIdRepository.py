from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        acacUserId: str | None = '1274825203',
        albeeesUserId: str | None = '61963795',
        aneevUserId: str | None = '1284413302',
        anivUserId: str | None = '749050409',
        ayAerithUserId: str | None = '277720347',
        bastionBlueUserId: str | None = '134639294',
        charlesUserId: str | None = '74350217',
        dylanStewUserId: str | None = '66822320',
        eddieUserId: str | None = '22587336',
        hokkaidoubareUserId: str | None = '490529357',
        imytUserId: str | None = '20037000',
        jrpUserId: str | None = '47768842',
        kiawaBotUserId: str | None = '786820295',
        lucentUserId: str | None = '30992900',
        mandooBotUserId: str | None = '761337972',
        merttUserId: str | None = '76798688',
        miaGuwuUserId: str | None = '176071941',
        oathyBotUserId: str | None = '147389114',
        patLanicusUserId: str | None = '46826466',
        stashiocatUserId: str | None = '20889981',
        volwrathUserId: str | None = '40463997',
        zanianUserId: str | None = '57704009',
    ):
        if acacUserId is not None and not isinstance(acacUserId, str):
            raise TypeError(f'acacUserId argument is malformed: \"{acacUserId}\"')
        elif albeeesUserId is not None and not isinstance(albeeesUserId, str):
            raise TypeError(f'albeeesUserId argument is malformed: \"{albeeesUserId}\"')
        elif aneevUserId is not None and not isinstance(aneevUserId, str):
            raise TypeError(f'aneevUserId argument is malformed: \"{aneevUserId}\"')
        elif anivUserId is not None and not isinstance(anivUserId, str):
            raise TypeError(f'anivUserId argument is malformed: \"{anivUserId}\"')
        elif ayAerithUserId is not None and not isinstance(ayAerithUserId, str):
            raise TypeError(f'ayAerithUserId argument is malformed: \"{ayAerithUserId}\"')
        elif bastionBlueUserId is not None and not isinstance(bastionBlueUserId, str):
            raise TypeError(f'bastionBlueUserId argument is malformed: \"{bastionBlueUserId}\"')
        elif charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')
        elif dylanStewUserId is not None and not isinstance(dylanStewUserId, str):
            raise TypeError(f'dylanStewUserId argument is malformed: \"{dylanStewUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddieUserId argument is malformed: \"{eddieUserId}\"')
        elif hokkaidoubareUserId is not None and not isinstance(hokkaidoubareUserId, str):
            raise TypeError(f'hokkaidoubareUserId argument is malformed: \"{hokkaidoubareUserId}\"')
        elif imytUserId is not None and not isinstance(imytUserId, str):
            raise TypeError(f'imytUserId argument is malformed: \"{imytUserId}\"')
        elif jrpUserId is not None and not isinstance(jrpUserId, str):
            raise TypeError(f'jrpUserId argument is malformed: \"{jrpUserId}\"')
        elif kiawaBotUserId is not None and not isinstance(kiawaBotUserId, str):
            raise TypeError(f'kiawaBotUserId argument is malformed: \"{kiawaBotUserId}\"')
        elif lucentUserId is not None and not isinstance(lucentUserId, str):
            raise TypeError(f'lucentUserId argument is malformed: \"{lucentUserId}\"')
        elif mandooBotUserId is not None and not isinstance(mandooBotUserId, str):
            raise TypeError(f'mandooBotUserId argument is malformed: \"{mandooBotUserId}\"')
        elif merttUserId is not None and not isinstance(merttUserId, str):
            raise TypeError(f'merttUserId argument is malformed: \"{merttUserId}\"')
        elif miaGuwuUserId is not None and not isinstance(miaGuwuUserId, str):
            raise TypeError(f'miaGuwuUserId argument is malformed: \"{miaGuwuUserId}\"')
        elif oathyBotUserId is not None and not isinstance(oathyBotUserId, str):
            raise TypeError(f'oathyBotUserId argument is malformed: \"{oathyBotUserId}\"')
        elif patLanicusUserId is not None and not isinstance(patLanicusUserId, str):
            raise TypeError(f'patLanicusUserId argument is malformed: \"{patLanicusUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')
        elif volwrathUserId is not None and not isinstance(volwrathUserId, str):
            raise TypeError(f'volwrathUserId argument is malformed: \"{volwrathUserId}\"')
        elif zanianUserId is not None and not isinstance(zanianUserId, str):
            raise TypeError(f'zanianUserId argument is malformed: \"{zanianUserId}\"')

        self.__acacUserId: str | None = acacUserId
        self.__albeeesUserId: str | None = albeeesUserId
        self.__aneevUserId: str | None = aneevUserId
        self.__anivUserId: str | None = anivUserId
        self.__ayAerithUserId: str | None = ayAerithUserId
        self.__bastionBlueUserId: str | None = bastionBlueUserId
        self.__charlesUserId: str | None = charlesUserId
        self.__dylanStewUserId: str | None = dylanStewUserId
        self.__eddieUserId: str | None = eddieUserId
        self.__hokkaidoubareUserId: str | None = hokkaidoubareUserId
        self.__imytUserId: str | None = imytUserId
        self.__jrpUserId: str | None = jrpUserId
        self.__kiawaBotUserId: str | None = kiawaBotUserId
        self.__lucentUserId: str | None = lucentUserId
        self.__mandooBotUserId: str | None = mandooBotUserId
        self.__merttUserId: str | None = merttUserId
        self.__miaGuwuUserId: str | None = miaGuwuUserId
        self.__oathyBotUserId: str | None = oathyBotUserId
        self.__patLanicusUserId: str | None = patLanicusUserId
        self.__stashiocatUserId: str | None = stashiocatUserId
        self.__volwrathUserId: str | None = volwrathUserId
        self.__zanianUserId: str | None = zanianUserId

    async def getAcacUserId(self) -> str | None:
        return self.__acacUserId

    async def getAlbeeesUserId(self) -> str | None:
        return self.__albeeesUserId

    async def getAneevUserId(self) -> str | None:
        return self.__aneevUserId

    async def getAnivUserId(self) -> str | None:
        return self.__anivUserId

    async def getAyAerithUserId(self) -> str | None:
        return self.__ayAerithUserId

    async def getBastionBlueUserId(self) -> str | None:
        return self.__bastionBlueUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId

    async def getDylanStewUserId(self) -> str | None:
        return self.__dylanStewUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getHokkaidoubareUserId(self) -> str | None:
        return self.__hokkaidoubareUserId

    async def getImytUserId(self) -> str | None:
        return self.__imytUserId

    async def getJrpUserId(self) -> str | None:
        return self.__jrpUserId

    async def getKiawaBotUserId(self) -> str | None:
        return self.__kiawaBotUserId

    async def getLucentUserId(self) -> str | None:
        return self.__lucentUserId

    async def getMandooBotUserId(self) -> str | None:
        return self.__mandooBotUserId

    async def getMerttUserId(self) -> str | None:
        return self.__merttUserId

    async def getMiaGuwuUserId(self) -> str | None:
        return self.__miaGuwuUserId

    async def getOathyBotUserId(self) -> str | None:
        return self.__oathyBotUserId

    async def getPatLanicusUserId(self) -> str | None:
        return self.__patLanicusUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId

    async def getVolwrathUserId(self) -> str | None:
        return self.__volwrathUserId

    async def getZanianUserId(self) -> str | None:
        return self.__zanianUserId
