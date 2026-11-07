from typing import Final

from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        beeblyBoopBotUserId: str | None = '812848264',
        blerpUserId: str | None = '253326823',
        boatWaifuUserId: str | None = '563334759',
        cynanBotUserId: str | None = '546457893',
        cynanBotTtsUserId: str | None = '977636741',
        disappointBotUserId: str | None = '169809959',
        frostyToolsDotComUserId: str | None = '955237329',
        funtoonUserId: str | None = '477393386',
        guwuBotUserId: str | None = '275323528',
        kazekiiBotUserId: str | None = '925014762',
        kiawaBotUserId: str | None = '786820295',
        mandooBotUserId: str | None = '761337972',
        minecraftUserId: str | None = '112568845',
        moobotUserId: str | None = '1564983',
        nightBotUserId: str | None = '19264788',
        oathyBotUserId: str | None = '147389114',
        puptimeUserId: str | None = '213177587',
        seryBotUserId: str | None = '402337290',
        soundAlertsUserId: str | None = '216527497',
        steineBotUserId: str | None = '1460771942',
        streamElementsUserId: str | None = '100135110',
        streamLabsUserId: str | None = '105166207',
        streamStickersUserId: str | None = '431026547',
        tangiaBotUserId: str | None = '853402143',
        teaTalkUserId: str | None = '479387514',
        theBinchBotUserId: str | None = '1053271950',
        theCatComputerUserId: str | None = '1326985885',
        theRunBotUserId: str | None = '795719761',
        twitchAccountUserId: str = '12826',
        twitchAnonymousGifterUserId: str = '274598607',
        valorantUserId: str | None = '490592527',
        zeldoBotUserId: str | None = '54866013',
        zoiiBotUserId: str | None = '188093207',
    ):
        if beeblyBoopBotUserId is not None and not isinstance(beeblyBoopBotUserId, str):
            raise TypeError(f'beeblyBoopBotUserId argument is malformed: \"{beeblyBoopBotUserId}\"')
        elif blerpUserId is not None and not isinstance(blerpUserId, str):
            raise TypeError(f'blerpUserId argument is malformed: \"{blerpUserId}\"')
        elif boatWaifuUserId is not None and not isinstance(boatWaifuUserId, str):
            raise TypeError(f'boatWaifuUserId argument is malformed: \"{boatWaifuUserId}\"')
        elif disappointBotUserId is not None and not isinstance(disappointBotUserId, str):
            raise TypeError(f'disappointBotUserId argument is malformed: \"{disappointBotUserId}\"')
        elif cynanBotUserId is not None and not isinstance(cynanBotUserId, str):
            raise TypeError(f'cynanBotUserId argument is malformed: \"{cynanBotUserId}\"')
        elif cynanBotTtsUserId is not None and not isinstance(cynanBotTtsUserId, str):
            raise TypeError(f'cynanBotTtsUserId argument is malformed: \"{cynanBotTtsUserId}\"')
        elif frostyToolsDotComUserId is not None and not isinstance(frostyToolsDotComUserId, str):
            raise TypeError(f'frostyToolsDotComUserId argument is malformed: \"{frostyToolsDotComUserId}\"')
        elif funtoonUserId is not None and not isinstance(funtoonUserId, str):
            raise TypeError(f'funtoonUserId argument is malformed: \"{funtoonUserId}\"')
        elif guwuBotUserId is not None and not isinstance(guwuBotUserId, str):
            raise TypeError(f'guwuBotUserId argument is malformed: \"{guwuBotUserId}\"')
        elif kazekiiBotUserId is not None and not isinstance(kazekiiBotUserId, str):
            raise TypeError(f'kazekiiBotUserId argument is malformed: \"{kazekiiBotUserId}\"')
        elif kiawaBotUserId is not None and not isinstance(kiawaBotUserId, str):
            raise TypeError(f'kiawaBotUserId argument is malformed: \"{kiawaBotUserId}\"')
        elif mandooBotUserId is not None and not isinstance(mandooBotUserId, str):
            raise TypeError(f'mandooBotUserId argument is malformed: \"{mandooBotUserId}\"')
        elif minecraftUserId is not None and not isinstance(minecraftUserId, str):
            raise TypeError(f'minecraftUserId argument is malformed: \"{minecraftUserId}\"')
        elif moobotUserId is not None and not isinstance(moobotUserId, str):
            raise TypeError(f'moobotUserId argument is malformed: \"{moobotUserId}\"')
        elif nightBotUserId is not None and not isinstance(nightBotUserId, str):
            raise TypeError(f'nightBotUserId argument is malformed: \"{nightBotUserId}\"')
        elif oathyBotUserId is not None and not isinstance(oathyBotUserId, str):
            raise TypeError(f'oathyBotUserId argument is malformed: \"{oathyBotUserId}\"')
        elif puptimeUserId is not None and not isinstance(puptimeUserId, str):
            raise TypeError(f'puptimeUserId argument is malformed: \"{puptimeUserId}\"')
        elif seryBotUserId is not None and not isinstance(seryBotUserId, str):
            raise TypeError(f'seryBotUserId argument is malformed: \"{seryBotUserId}\"')
        elif soundAlertsUserId is not None and not isinstance(soundAlertsUserId, str):
            raise TypeError(f'soundAlertsUserId argument is malformed: \"{soundAlertsUserId}\"')
        elif steineBotUserId is not None and not isinstance(steineBotUserId, str):
            raise TypeError(f'steineBotUserId argument is malformed: \"{steineBotUserId}\"')
        elif streamElementsUserId is not None and not isinstance(streamElementsUserId, str):
            raise TypeError(f'streamElementsUserId argument is malformed: \"{streamElementsUserId}\"')
        elif streamLabsUserId is not None and not isinstance(streamLabsUserId, str):
            raise TypeError(f'streamLabsUserId argument is malformed: \"{streamLabsUserId}\"')
        elif streamStickersUserId is not None and not isinstance(streamStickersUserId, str):
            raise TypeError(f'streamStickersUserId argument is malformed: \"{streamStickersUserId}\"')
        elif tangiaBotUserId is not None and not isinstance(tangiaBotUserId, str):
            raise TypeError(f'tangiaBotUserId argument is malformed: \"{tangiaBotUserId}\"')
        elif teaTalkUserId is not None and not isinstance(teaTalkUserId, str):
            raise TypeError(f'teaTalkUserId argument is malformed: \"{teaTalkUserId}\"')
        elif theBinchBotUserId is not None and not isinstance(theBinchBotUserId, str):
            raise TypeError(f'theBinchBotUserId argument is malformed: \"{theBinchBotUserId}\"')
        elif theCatComputerUserId is not None and not isinstance(theCatComputerUserId, str):
            raise TypeError(f'theCatComputerUserId argument is malformed: \"{theCatComputerUserId}\"')
        elif theRunBotUserId is not None and not isinstance(theRunBotUserId, str):
            raise TypeError(f'theRunBotUserId argument is malformed: \"{theRunBotUserId}\"')
        elif not utils.isValidStr(twitchAccountUserId):
            raise TypeError(f'twitchAccountUserId argument is malformed: \"{twitchAccountUserId}\"')
        elif not utils.isValidStr(twitchAnonymousGifterUserId):
            raise TypeError(f'twitchAnonymousGifterUserId argument is malformed: \"{twitchAnonymousGifterUserId}\"')
        elif valorantUserId is not None and not isinstance(valorantUserId, str):
            raise TypeError(f'valorantUserId argument is malformed: \"{valorantUserId}\"')
        elif zeldoBotUserId is not None and not isinstance(zeldoBotUserId, str):
            raise TypeError(f'zeldoBotUserId argument is malformed: \"{zeldoBotUserId}\"')
        elif zoiiBotUserId is not None and not isinstance(zoiiBotUserId, str):
            raise TypeError(f'zoiiBotUserId argument is malformed: \"{zoiiBotUserId}\"')

        self.__beeblyBoopBotUserId: Final[str | None] = beeblyBoopBotUserId
        self.__blerpUserId: Final[str | None] = blerpUserId
        self.__boatWaifuUserId: Final[str | None] = boatWaifuUserId
        self.__cynanBotUserId: Final[str | None] = cynanBotUserId
        self.__cynanBotTtsUserId: Final[str | None] = cynanBotTtsUserId
        self.__disappointBotUserId: Final[str | None] = disappointBotUserId
        self.__frostyToolsDotComUserId: Final[str | None] = frostyToolsDotComUserId
        self.__funtoonUserId: Final[str | None] = funtoonUserId
        self.__guwuBotUserId: Final[str | None] = guwuBotUserId
        self.__kazekiiBotUserId: Final[str | None] = kazekiiBotUserId
        self.__mandooBotUserId: Final[str | None] = mandooBotUserId
        self.__minecraftUserId: Final[str | None] = minecraftUserId
        self.__moobotUserId: Final[str | None] = moobotUserId
        self.__nightBotUserId: Final[str | None] = nightBotUserId
        self.__oathyBotUserId: Final[str | None] = oathyBotUserId
        self.__puptimeUserId: Final[str | None] = puptimeUserId
        self.__seryBotUserId: Final[str | None] = seryBotUserId
        self.__soundAlertsUserId: Final[str | None] = soundAlertsUserId
        self.__steineBotUserId: Final[str | None] = steineBotUserId
        self.__streamElementsUserId: Final[str | None] = streamElementsUserId
        self.__streamLabsUserId: Final[str | None] = streamLabsUserId
        self.__streamStickersUserId: Final[str | None] = streamStickersUserId
        self.__tangiaBotUserId: Final[str | None] = tangiaBotUserId
        self.__teaTalkUserId: Final[str | None] = teaTalkUserId
        self.__theBinchBotUserId: Final[str | None] = theBinchBotUserId
        self.__theCatComputerUserId: Final[str | None] = theCatComputerUserId
        self.__theRunBotUserId: Final[str | None] = theRunBotUserId
        self.__twitchAccountUserId: Final[str] = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: Final[str] = twitchAnonymousGifterUserId
        self.__valorantUserId: Final[str | None] = valorantUserId
        self.__zeldoBotUserId: Final[str | None] = zeldoBotUserId
        self.__zoiiBotUserId: Final[str | None] = zoiiBotUserId

    async def getAllUserIds(self) -> frozenset[str]:
        allUserIds: set[str] = set()

        beeblyBoopBotUserId = await self.getBeeblyBoopBotUserId()
        if utils.isValidStr(beeblyBoopBotUserId):
            allUserIds.add(beeblyBoopBotUserId)

        blerpUserId = await self.getBlerpUserId()
        if utils.isValidStr(blerpUserId):
            allUserIds.add(blerpUserId)

        boatWaifuUserId = await self.getBoatWaifuUserId()
        if utils.isValidStr(boatWaifuUserId):
            allUserIds.add(boatWaifuUserId)

        cynanBotUserId = await self.getCynanBotUserId()
        if utils.isValidStr(cynanBotUserId):
            allUserIds.add(cynanBotUserId)

        cynanBotTtsUserId = await self.getCynanBotTtsUserId()
        if utils.isValidStr(cynanBotTtsUserId):
            allUserIds.add(cynanBotTtsUserId)

        disappointBotUserId = await self.getDisappointBotUserId()
        if utils.isValidStr(disappointBotUserId):
            allUserIds.add(disappointBotUserId)

        frostyToolsDotComUserId = await self.getFrostyToolsDotComUserId()
        if utils.isValidStr(frostyToolsDotComUserId):
            allUserIds.add(frostyToolsDotComUserId)

        funtoonUserId = await self.getFuntoonUserId()
        if utils.isValidStr(funtoonUserId):
            allUserIds.add(funtoonUserId)

        kazekiiBotUserId = await self.getKazekiiBotUserId()
        if utils.isValidStr(kazekiiBotUserId):
            allUserIds.add(kazekiiBotUserId)

        mandooBotUserId = await self.getMandooBotUserId()
        if utils.isValidStr(mandooBotUserId):
            allUserIds.add(mandooBotUserId)

        minecraftUserId = await self.getMinecraftUserId()
        if utils.isValidStr(minecraftUserId):
            allUserIds.add(minecraftUserId)

        moobotUserId = await self.getMoobotUserId()
        if utils.isValidStr(moobotUserId):
            allUserIds.add(moobotUserId)

        nightBotUserId = await self.getNightbotUserId()
        if utils.isValidStr(nightBotUserId):
            allUserIds.add(nightBotUserId)

        puptimeUserId = await self.getPuptimeUserId()
        if utils.isValidStr(puptimeUserId):
            allUserIds.add(puptimeUserId)

        seryBotUserId = await self.getSeryBotUserId()
        if utils.isValidStr(seryBotUserId):
            allUserIds.add(seryBotUserId)

        soundAlertsUserId = await self.getSoundAlertsUserId()
        if utils.isValidStr(soundAlertsUserId):
            allUserIds.add(soundAlertsUserId)

        steineBotUserId = await self.getSteineBotUserId()
        if utils.isValidStr(steineBotUserId):
            allUserIds.add(steineBotUserId)

        streamElementsUserId = await self.getStreamElementsUserId()
        if utils.isValidStr(streamElementsUserId):
            allUserIds.add(streamElementsUserId)

        streamLabsUserId = await self.getStreamLabsUserId()
        if utils.isValidStr(streamLabsUserId):
            allUserIds.add(streamLabsUserId)

        streamStickersUserId = await self.getStreamStickersUserId()
        if utils.isValidStr(streamStickersUserId):
            allUserIds.add(streamStickersUserId)

        tangiaBotUserId = await self.getTangiaBotUserId()
        if utils.isValidStr(tangiaBotUserId):
            allUserIds.add(tangiaBotUserId)

        teaTalkUserId = await self.getTeaTalkUserId()
        if utils.isValidStr(teaTalkUserId):
            allUserIds.add(teaTalkUserId)

        theBinchBotUserId = await self.getTheBinchBotUserId()
        if utils.isValidStr(theBinchBotUserId):
            allUserIds.add(theBinchBotUserId)

        theCatComputerUserId = await self.getTheCatComputerUserId()
        if utils.isValidStr(theCatComputerUserId):
            allUserIds.add(theCatComputerUserId)

        theRunBotUserId = await self.getTheRunBotUserId()
        if utils.isValidStr(theRunBotUserId):
            allUserIds.add(theRunBotUserId)

        twitchAccountUserId = await self.getTwitchAccountUserId()
        allUserIds.add(twitchAccountUserId)

        twitchAnonymousGifterUserId = await self.getTwitchAnonymousGifterUserId()
        allUserIds.add(twitchAnonymousGifterUserId)

        valorantUserId = await self.getValorantUserId()
        if utils.isValidStr(valorantUserId):
            allUserIds.add(valorantUserId)

        zeldoBotUserId = await self.getZeldoBotUserId()
        if utils.isValidStr(zeldoBotUserId):
            allUserIds.add(zeldoBotUserId)

        zoiiBotUserId = await self.getZoiiBotUserId()
        if utils.isValidStr(zoiiBotUserId):
            allUserIds.add(zoiiBotUserId)

        return frozenset(allUserIds)

    async def getBeeblyBoopBotUserId(self) -> str | None:
        return self.__beeblyBoopBotUserId

    async def getBlerpUserId(self) -> str | None:
        return self.__blerpUserId

    async def getBoatWaifuUserId(self) -> str | None:
        return self.__boatWaifuUserId

    async def getCynanBotUserId(self) -> str | None:
        return self.__cynanBotUserId

    async def getCynanBotTtsUserId(self) -> str | None:
        return self.__cynanBotTtsUserId

    async def getDisappointBotUserId(self) -> str | None:
        return self.__disappointBotUserId

    async def getFrostyToolsDotComUserId(self) -> str | None:
        return self.__frostyToolsDotComUserId

    async def getFuntoonUserId(self) -> str | None:
        return self.__funtoonUserId

    async def getGuwuBotUserId(self) -> str | None:
        return self.__guwuBotUserId

    async def getKazekiiBotUserId(self) -> str | None:
        return self.__kazekiiBotUserId

    async def getMandooBotUserId(self) -> str | None:
        return self.__mandooBotUserId

    async def getMinecraftUserId(self) -> str | None:
        return self.__minecraftUserId

    async def getMoobotUserId(self) -> str | None:
        return self.__moobotUserId

    async def getNightbotUserId(self) -> str | None:
        return self.__nightBotUserId

    async def getOathyBotUserId(self) -> str | None:
        return self.__oathyBotUserId

    async def getPuptimeUserId(self) -> str | None:
        return self.__puptimeUserId

    async def getSeryBotUserId(self) -> str | None:
        return self.__seryBotUserId

    async def getSoundAlertsUserId(self) -> str | None:
        return self.__soundAlertsUserId

    async def getSteineBotUserId(self) -> str | None:
        return self.__steineBotUserId

    async def getStreamElementsUserId(self) -> str | None:
        return self.__streamElementsUserId

    async def getStreamLabsUserId(self) -> str | None:
        return self.__streamLabsUserId

    async def getStreamStickersUserId(self) -> str | None:
        return self.__streamStickersUserId

    async def getTangiaBotUserId(self) -> str | None:
        return self.__tangiaBotUserId

    async def getTeaTalkUserId(self) -> str | None:
        return self.__teaTalkUserId

    async def getTheBinchBotUserId(self) -> str | None:
        return self.__theBinchBotUserId

    async def getTheCatComputerUserId(self) -> str | None:
        return self.__theCatComputerUserId

    async def getTheRunBotUserId(self) -> str | None:
        return self.__theRunBotUserId

    async def getTwitchAccountUserId(self) -> str:
        return self.__twitchAccountUserId

    async def getTwitchAnonymousGifterUserId(self) -> str:
        return self.__twitchAnonymousGifterUserId

    async def getValorantUserId(self) -> str | None:
        return self.__valorantUserId

    async def getZeldoBotUserId(self) -> str | None:
        return self.__zeldoBotUserId

    async def getZoiiBotUserId(self) -> str | None:
        return self.__zoiiBotUserId
