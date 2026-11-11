from typing import Final

from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        albeeesUserId: str | None = '61963795',
        amySumisuUserId: str | None = '526746071',
        angieYunaUserId: str | None = '55374172',
        aoyamabukiUserId: str | None = '600886831',
        ayAerithUserId: str | None = '277720347',
        bastionBlueUserId: str | None = '134639294',
        behemothUserId: str | None = '30347212',
        charlyUserId: str | None = '74350217',
        concisionUserId: str | None = '56778682',
        deltaRayneUserId: str | None = '195145575',
        dylanStewUserId: str | None = '66822320',
        eddieUserId: str | None = '22587336',
        edenUserId: str | None = '46081042',
        etucaUserId: str | None = '20339523',
        garUserId: str | None = '19529144',
        harleyHardtUserId: str | None = '1140926612',
        hokkaidoubareUserId: str | None = '490529357',
        imytUserId: str | None = '20037000',
        jrpUserId: str | None = '47768842',
        kazekiiUserId: str | None = '62963382',
        kiaraUserId: str | None = '37055465',
        lndegenUserId: str | None = '63602335',
        lucyUserId: str | None = '30992900',
        merttUserId: str | None = '76798688',
        miaGuwuUserId: str | None = '176071941',
        nevdiUserId: str | None = '41499302',
        nintendesiUserId: str | None = '150066920',
        oatsngoatsUserId: str | None = '39886669',
        patLanicusUserId: str | None = '46826466',
        sakuraMilkTeaUserId: str | None = '183436307',
        shinyZeniUserId: str | None = '137176010',
        stashiocatUserId: str | None = '20889981',
        tawUserId: str | None = '32465208',
        tsteineUserId: str | None = '18944536',
        twinmoUserId: str | None = '431483293',
        volwrathUserId: str | None = '40463997',
        zanianUserId: str | None = '57704009',
        zoastyUserId: str | None = '28665562',
    ):
        if albeeesUserId is not None and not isinstance(albeeesUserId, str):
            raise TypeError(f'albeeesUserId argument is malformed: \"{albeeesUserId}\"')
        elif amySumisuUserId is not None and not isinstance(amySumisuUserId, str):
            raise TypeError(f'amySumisuUserId argument is malformed: \"{amySumisuUserId}\"')
        elif angieYunaUserId is not None and not isinstance(angieYunaUserId, str):
            raise TypeError(f'angieYunaUserId argument is malformed: \"{angieYunaUserId}\"')
        elif aoyamabukiUserId is not None and not isinstance(aoyamabukiUserId, str):
            raise TypeError(f'aoyamabukiUserId argument is malformed: \"{aoyamabukiUserId}\"')
        elif ayAerithUserId is not None and not isinstance(ayAerithUserId, str):
            raise TypeError(f'ayAerithUserId argument is malformed: \"{ayAerithUserId}\"')
        elif bastionBlueUserId is not None and not isinstance(bastionBlueUserId, str):
            raise TypeError(f'bastionBlueUserId argument is malformed: \"{bastionBlueUserId}\"')
        elif behemothUserId is not None and not isinstance(behemothUserId, str):
            raise TypeError(f'behemothUserId argument is malformed: \"{behemothUserId}\"')
        elif charlyUserId is not None and not isinstance(charlyUserId, str):
            raise TypeError(f'charlyUserId argument is malformed: \"{charlyUserId}\"')
        elif concisionUserId is not None and not isinstance(concisionUserId, str):
            raise TypeError(f'concisionUserId argument is malformed: \"{concisionUserId}\"')
        elif deltaRayneUserId is not None and not isinstance(deltaRayneUserId, str):
            raise TypeError(f'deltaRayneUserId argument is malformed: \"{deltaRayneUserId}\"')
        elif dylanStewUserId is not None and not isinstance(dylanStewUserId, str):
            raise TypeError(f'dylanStewUserId argument is malformed: \"{dylanStewUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddieUserId argument is malformed: \"{eddieUserId}\"')
        elif edenUserId is not None and not isinstance(edenUserId, str):
            raise TypeError(f'edenUserId argument is malformed: \"{edenUserId}\"')
        elif etucaUserId is not None and not isinstance(etucaUserId, str):
            raise TypeError(f'etucaUserId argument is malformed: \"{etucaUserId}\"')
        elif garUserId is not None and not isinstance(garUserId, str):
            raise TypeError(f'garUserId argument is malformed: \"{garUserId}\"')
        elif harleyHardtUserId is not None and not isinstance(harleyHardtUserId, str):
            raise TypeError(f'harleyHardtUserId argument is malformed: \"{harleyHardtUserId}\"')
        elif hokkaidoubareUserId is not None and not isinstance(hokkaidoubareUserId, str):
            raise TypeError(f'hokkaidoubareUserId argument is malformed: \"{hokkaidoubareUserId}\"')
        elif imytUserId is not None and not isinstance(imytUserId, str):
            raise TypeError(f'imytUserId argument is malformed: \"{imytUserId}\"')
        elif jrpUserId is not None and not isinstance(jrpUserId, str):
            raise TypeError(f'jrpUserId argument is malformed: \"{jrpUserId}\"')
        elif kazekiiUserId is not None and not isinstance(kazekiiUserId, str):
            raise TypeError(f'kazekiiUserId argument is malformed: \"{kazekiiUserId}\"')
        elif kiaraUserId is not None and not isinstance(kiaraUserId, str):
            raise TypeError(f'kiaraUserId argument is malformed: \"{kiaraUserId}\"')
        elif lndegenUserId is not None and not isinstance(lndegenUserId, str):
            raise TypeError(f'lndegenUserId argument is malformed: \"{lndegenUserId}\"')
        elif lucyUserId is not None and not isinstance(lucyUserId, str):
            raise TypeError(f'lucyUserId argument is malformed: \"{lucyUserId}\"')
        elif merttUserId is not None and not isinstance(merttUserId, str):
            raise TypeError(f'merttUserId argument is malformed: \"{merttUserId}\"')
        elif miaGuwuUserId is not None and not isinstance(miaGuwuUserId, str):
            raise TypeError(f'miaGuwuUserId argument is malformed: \"{miaGuwuUserId}\"')
        elif nevdiUserId is not None and not isinstance(nevdiUserId, str):
            raise TypeError(f'nevdiUserId argument is malformed: \"{nevdiUserId}\"')
        elif nintendesiUserId is not None and not isinstance(nintendesiUserId, str):
            raise TypeError(f'nintendesiUserId argument is malformed: \"{nintendesiUserId}\"')
        elif oatsngoatsUserId is not None and not isinstance(oatsngoatsUserId, str):
            raise TypeError(f'oatsngoatsUserId argument is malformed: \"{oatsngoatsUserId}\"')
        elif patLanicusUserId is not None and not isinstance(patLanicusUserId, str):
            raise TypeError(f'patLanicusUserId argument is malformed: \"{patLanicusUserId}\"')
        elif sakuraMilkTeaUserId is not None and not isinstance(sakuraMilkTeaUserId, str):
            raise TypeError(f'sakuraMilkTeaUserId argument is malformed: \"{sakuraMilkTeaUserId}\"')
        elif shinyZeniUserId is not None and not isinstance(shinyZeniUserId, str):
            raise TypeError(f'shinyZeniUserId argument is malformed: \"{shinyZeniUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')
        elif tawUserId is not None and not isinstance(tawUserId, str):
            raise TypeError(f'tawUserId argument is malformed: \"{tawUserId}\"')
        elif tsteineUserId is not None and not isinstance(tsteineUserId, str):
            raise TypeError(f'tsteineUserId argument is malformed: \"{tsteineUserId}\"')
        elif twinmoUserId is not None and not isinstance(twinmoUserId, str):
            raise TypeError(f'twinmoUserId argument is malformed: \"{twinmoUserId}\"')
        elif volwrathUserId is not None and not isinstance(volwrathUserId, str):
            raise TypeError(f'volwrathUserId argument is malformed: \"{volwrathUserId}\"')
        elif zanianUserId is not None and not isinstance(zanianUserId, str):
            raise TypeError(f'zanianUserId argument is malformed: \"{zanianUserId}\"')
        elif zoastyUserId is not None and not isinstance(zoastyUserId, str):
            raise TypeError(f'zoastyUserId argument is malformed: \"{zoastyUserId}\"')

        self.__albeeesUserId: Final[str | None] = albeeesUserId
        self.__amySumisuUserId: Final[str | None] = amySumisuUserId
        self.__angieYunaUserId: Final[str |  None] = angieYunaUserId
        self.__aoyamabukiUserId: Final[str | None] = aoyamabukiUserId
        self.__ayAerithUserId: Final[str | None] = ayAerithUserId
        self.__bastionBlueUserId: Final[str | None] = bastionBlueUserId
        self.__behemothUserId: Final[str | None] = behemothUserId
        self.__charlyUserId: Final[str | None] = charlyUserId
        self.__concisionUserId: Final[str | None] = concisionUserId
        self.__deltaRayneUserId: Final[str | None] = deltaRayneUserId
        self.__dylanStewUserId: Final[str | None] = dylanStewUserId
        self.__eddieUserId: Final[str | None] = eddieUserId
        self.__edenUserId: Final[str | None] = edenUserId
        self.__etucaUserId: Final[str | None] = etucaUserId
        self.__garUserId: Final[str | None] = garUserId
        self.__harleyHardtUserId: Final[str | None] = harleyHardtUserId
        self.__hokkaidoubareUserId: Final[str | None] = hokkaidoubareUserId
        self.__imytUserId: Final[str | None] = imytUserId
        self.__jrpUserId: Final[str | None] = jrpUserId
        self.__kazekiiUserId: Final[str | None] = kazekiiUserId
        self.__kiaraUserId: Final[str | None] = kiaraUserId
        self.__lndegenUserId: Final[str | None] = lndegenUserId
        self.__lucyUserId: Final[str | None] = lucyUserId
        self.__merttUserId: Final[str | None] = merttUserId
        self.__miaGuwuUserId: Final[str | None] = miaGuwuUserId
        self.__nevdiUserId: Final[str | None] = nevdiUserId
        self.__nintendesiUserId: Final[str | None] = nintendesiUserId
        self.__oatsngoatsUserId: Final[str | None] = oatsngoatsUserId
        self.__patLanicusUserId: Final[str | None] = patLanicusUserId
        self.__sakuraMilkTeaUserId: Final[str | None] = sakuraMilkTeaUserId
        self.__shinyZeniUserId: Final[str | None] = shinyZeniUserId
        self.__stashiocatUserId: Final[str | None] = stashiocatUserId
        self.__tawUserId: Final[str | None] = tawUserId
        self.__tsteineUserId: Final[str | None] = tsteineUserId
        self.__twinmoUserId: Final[str | None] = twinmoUserId
        self.__volwrathUserId: Final[str | None] = volwrathUserId
        self.__zanianUserId: Final[str | None] = zanianUserId
        self.__zoastyUserId: Final[str | None] = zoastyUserId

    async def getAlbeeesUserId(self) -> str | None:
        return self.__albeeesUserId

    async def getAmySumisuUserId(self) -> str | None:
        return self.__amySumisuUserId

    async def getAngieYunaUserId(self) -> str | None:
        return self.__angieYunaUserId

    async def getAoyamabukiUserId(self) -> str | None:
        return self.__aoyamabukiUserId

    async def getAyAerithUserId(self) -> str | None:
        return self.__ayAerithUserId

    async def getBastionBlueUserId(self) -> str | None:
        return self.__bastionBlueUserId

    async def getBehemothUserId(self) -> str | None:
        return self.__behemothUserId

    async def getCharlyUserId(self) -> str | None:
        return self.__charlyUserId

    async def getConcisionUserId(self) -> str | None:
        return self.__concisionUserId

    async def getDeltaRayneUserId(self) -> str | None:
        return self.__deltaRayneUserId

    async def getDylanStewUserId(self) -> str | None:
        return self.__dylanStewUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getEdenUserId(self) -> str | None:
        return self.__edenUserId

    async def getEtucaUserId(self) -> str | None:
        return self.__etucaUserId

    async def getGarUserId(self) -> str | None:
        return self.__garUserId

    async def getHarleyHardtUserId(self) -> str | None:
        return self.__harleyHardtUserId

    async def getHokkaidoubareUserId(self) -> str | None:
        return self.__hokkaidoubareUserId

    async def getImytUserId(self) -> str | None:
        return self.__imytUserId

    async def getJrpUserId(self) -> str | None:
        return self.__jrpUserId

    async def getKazekiiUserId(self) -> str | None:
        return self.__kazekiiUserId

    async def getKiaraUserId(self) -> str | None:
        return self.__kiaraUserId

    async def getLndegenUserId(self) -> str | None:
        return self.__lndegenUserId

    async def getLucyUserId(self) -> str | None:
        return self.__lucyUserId

    async def getMerttUserId(self) -> str | None:
        return self.__merttUserId

    async def getMiaGuwuUserId(self) -> str | None:
        return self.__miaGuwuUserId

    async def getNevdiUserId(self) -> str | None:
        return self.__nevdiUserId

    async def getNintendesiUserId(self) -> str | None:
        return self.__nintendesiUserId

    async def getOatsngoatsUserId(self) -> str | None:
        return self.__oatsngoatsUserId

    async def getPatLanicusUserId(self) -> str | None:
        return self.__patLanicusUserId

    async def getSakuraMilkTeaUserId(self) -> str | None:
        return self.__sakuraMilkTeaUserId

    async def getShinyZeniUserId(self) -> str | None:
        return self.__shinyZeniUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId

    async def getTawUserId(self) -> str | None:
        return self.__tawUserId

    async def getTsteineUserId(self) -> str | None:
        return self.__tsteineUserId

    async def getTwinmoUserId(self) -> str | None:
        return self.__twinmoUserId

    async def getVolwrathUserId(self) -> str | None:
        return self.__volwrathUserId

    async def getZanianUserId(self) -> str | None:
        return self.__zanianUserId

    async def getZoastyUserId(self) -> str | None:
        return self.__zoastyUserId
