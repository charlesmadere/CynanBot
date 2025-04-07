from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        nightBotUserId: str | None = '19264788',
        puptimeUserId: str | None = '213177587',
        seryBotUserId: str | None = '402337290',
        soundAlertsUserId: str | None = '216527497',
        streamElementsUserId: str | None = '100135110',
        streamLabsUserId: str | None = '105166207',
        tangiaBotUserId: str | None = '853402143',
        theRunBotUserId: str | None = '795719761',
        twitchAccountUserId: str = '12826',
        twitchAnonymousGifterUserId: str = '274598607',
        valorantUserId: str | None = '490592527'
    ):
        if nightBotUserId is not None and not isinstance(nightBotUserId, str):
            raise TypeError(f'nightBotUserId argument is malformed: \"{nightBotUserId}\"')
        if puptimeUserId is not None and not isinstance(puptimeUserId, str):
            raise TypeError(f'puptimeUserId argument is malformed: \"{puptimeUserId}\"')
        elif seryBotUserId is not None and not isinstance(seryBotUserId, str):
            raise TypeError(f'seryBotUserId argument is malformed: \"{seryBotUserId}\"')
        elif soundAlertsUserId is not None and not isinstance(soundAlertsUserId, str):
            raise TypeError(f'soundAlertsUserId argument is malformed: \"{soundAlertsUserId}\"')
        elif streamElementsUserId is not None and not isinstance(streamElementsUserId, str):
            raise TypeError(f'streamElementsUserId argument is malformed: \"{streamElementsUserId}\"')
        elif streamLabsUserId is not None and not isinstance(streamLabsUserId, str):
            raise TypeError(f'streamLabsUserId argument is malformed: \"{streamLabsUserId}\"')
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

        self.__nightBotUserId: str | None = nightBotUserId
        self.__puptimeUserId: str | None = puptimeUserId
        self.__seryBotUserId: str | None = seryBotUserId
        self.__soundAlertsUserId: str | None = soundAlertsUserId
        self.__streamElementsUserId: str | None = streamElementsUserId
        self.__streamLabsUserId: str | None = streamLabsUserId
        self.__tangiaBotUserId: str | None = tangiaBotUserId
        self.__theRunBotUserId: str | None = theRunBotUserId
        self.__twitchAccountUserId: str = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: str = twitchAnonymousGifterUserId
        self.__valorantUserId: str | None = valorantUserId

    async def getAllUserIds(self) -> frozenset[str]:
        allUserIds: set[str] = set()

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

        return frozenset(allUserIds)

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
