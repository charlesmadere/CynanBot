from typing import Final

from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        frostyToolsDotComUserId: str | None = '955237329',
        moobotUserId: str | None = '1564983',
        nightBotUserId: str | None = '19264788',
        puptimeUserId: str | None = '213177587',
        seryBotUserId: str | None = '402337290',
        soundAlertsUserId: str | None = '216527497',
        streamElementsUserId: str | None = '100135110',
        streamLabsUserId: str | None = '105166207',
        streamStickersUserId: str | None = '431026547',
        tangiaBotUserId: str | None = '853402143',
        theRunBotUserId: str | None = '795719761',
        twitchAccountUserId: str = '12826',
        twitchAnonymousGifterUserId: str = '274598607',
        valorantUserId: str | None = '490592527',
        zeldoBotUserId: str | None = '54866013',
    ):
        if frostyToolsDotComUserId is not None and not isinstance(frostyToolsDotComUserId, str):
            raise TypeError(f'frostyToolsDotComUserId argument is malformed: \"{frostyToolsDotComUserId}\"')
        elif moobotUserId is not None and not isinstance(moobotUserId, str):
            raise TypeError(f'moobotUserId argument is malformed: \"{moobotUserId}\"')
        elif nightBotUserId is not None and not isinstance(nightBotUserId, str):
            raise TypeError(f'nightBotUserId argument is malformed: \"{nightBotUserId}\"')
        elif puptimeUserId is not None and not isinstance(puptimeUserId, str):
            raise TypeError(f'puptimeUserId argument is malformed: \"{puptimeUserId}\"')
        elif seryBotUserId is not None and not isinstance(seryBotUserId, str):
            raise TypeError(f'seryBotUserId argument is malformed: \"{seryBotUserId}\"')
        elif soundAlertsUserId is not None and not isinstance(soundAlertsUserId, str):
            raise TypeError(f'soundAlertsUserId argument is malformed: \"{soundAlertsUserId}\"')
        elif streamElementsUserId is not None and not isinstance(streamElementsUserId, str):
            raise TypeError(f'streamElementsUserId argument is malformed: \"{streamElementsUserId}\"')
        elif streamLabsUserId is not None and not isinstance(streamLabsUserId, str):
            raise TypeError(f'streamLabsUserId argument is malformed: \"{streamLabsUserId}\"')
        elif streamStickersUserId is not None and not isinstance(streamStickersUserId, str):
            raise TypeError(f'streamStickersUserId argument is malformed: \"{streamStickersUserId}\"')
        elif tangiaBotUserId is not None and not isinstance(tangiaBotUserId, str):
            raise TypeError(f'tangiaBotUserId argument is malformed: \"{tangiaBotUserId}\"')
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

        self.__frostyToolsDotComUserId: Final[str | None] = frostyToolsDotComUserId
        self.__moobotUserId: Final[str | None] = moobotUserId
        self.__nightBotUserId: Final[str | None] = nightBotUserId
        self.__puptimeUserId: Final[str | None] = puptimeUserId
        self.__seryBotUserId: Final[str | None] = seryBotUserId
        self.__soundAlertsUserId: Final[str | None] = soundAlertsUserId
        self.__streamElementsUserId: Final[str | None] = streamElementsUserId
        self.__streamLabsUserId: Final[str | None] = streamLabsUserId
        self.__streamStickersUserId: Final[str | None] = streamStickersUserId
        self.__tangiaBotUserId: Final[str | None] = tangiaBotUserId
        self.__theRunBotUserId: Final[str | None] = theRunBotUserId
        self.__twitchAccountUserId: Final[str] = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: Final[str] = twitchAnonymousGifterUserId
        self.__valorantUserId: Final[str | None] = valorantUserId
        self.__zeldoBotUserId: Final[str | None] = zeldoBotUserId

    async def getAllUserIds(self) -> frozenset[str]:
        allUserIds: set[str] = set()

        frostyToolsDotComUserId = await self.getFrostyToolsDotComUserId()
        if utils.isValidStr(frostyToolsDotComUserId):
            allUserIds.add(frostyToolsDotComUserId)

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

        return frozenset(allUserIds)

    async def getFrostyToolsDotComUserId(self) -> str | None:
        return self.__frostyToolsDotComUserId

    async def getMoobotUserId(self) -> str | None:
        return self.__moobotUserId

    async def getNightbotUserId(self) -> str | None:
        return self.__nightBotUserId

    async def getPuptimeUserId(self) -> str | None:
        return self.__puptimeUserId

    async def getSeryBotUserId(self) -> str | None:
        return self.__seryBotUserId

    async def getSoundAlertsUserId(self) -> str | None:
        return self.__soundAlertsUserId

    async def getStreamElementsUserId(self) -> str | None:
        return self.__streamElementsUserId

    async def getStreamLabsUserId(self) -> str | None:
        return self.__streamLabsUserId

    async def getStreamStickersUserId(self) -> str | None:
        return self.__streamStickersUserId

    async def getTangiaBotUserId(self) -> str | None:
        return self.__tangiaBotUserId

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
