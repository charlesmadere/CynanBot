from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        soundAlertsUserId: str | None = '216527497',
        twitchAccountUserId: str = '12826',
        twitchAnonymousGifterUserId: str = '274598607',
        valorantUserId: str | None = '490592527'
    ):
        if soundAlertsUserId is not None and not isinstance(soundAlertsUserId, str):
            raise TypeError(f'soundAlertsUserId argument is malformed: \"{soundAlertsUserId}\"')
        elif not utils.isValidStr(twitchAccountUserId):
            raise TypeError(f'twitchAccountUserId argument is malformed: \"{twitchAccountUserId}\"')
        elif not utils.isValidStr(twitchAnonymousGifterUserId):
            raise TypeError(f'twitchAnonymousGifterUserId argument is malformed: \"{twitchAnonymousGifterUserId}\"')
        elif valorantUserId is not None and not isinstance(valorantUserId, str):
            raise TypeError(f'valorantUserId argument is malformed: \"{valorantUserId}\"')

        self.__soundAlertsUserId: str | None = soundAlertsUserId
        self.__twitchAccountUserId: str = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: str = twitchAnonymousGifterUserId
        self.__valorantUserId: str | None = valorantUserId

    async def getSoundAlertsUserId(self) -> str | None:
        return self.__soundAlertsUserId

    async def getTwitchAccountUserId(self) -> str:
        return self.__twitchAccountUserId

    async def getTwitchAnonymousGifterUserId(self) -> str:
        return self.__twitchAnonymousGifterUserId

    async def getValorantUserId(self) -> str | None:
        return self.__valorantUserId
