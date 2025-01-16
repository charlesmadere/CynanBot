from .officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ...misc import utils as utils


class OfficialTwitchAccountUserIdProvider(OfficialTwitchAccountUserIdProviderInterface):

    def __init__(
        self,
        twitchAccountUserId: str = '12826',
        twitchAnonymousGifterUserId: str = '274598607',
        valorantUserId: str = '490592527'
    ):
        if not utils.isValidStr(twitchAccountUserId):
            raise TypeError(f'twitchAccountUserId argument is malformed: \"{twitchAccountUserId}\"')
        elif not utils.isValidStr(twitchAnonymousGifterUserId):
            raise TypeError(f'twitchAnonymousGifterUserId argument is malformed: \"{twitchAnonymousGifterUserId}\"')
        elif not utils.isValidStr(valorantUserId):
            raise TypeError(f'valorantUserId argument is malformed: \"{valorantUserId}\"')

        self.__twitchAccountUserId: str = twitchAccountUserId
        self.__twitchAnonymousGifterUserId: str = twitchAnonymousGifterUserId
        self.__valorantUserId: str = valorantUserId

    async def getTwitchAccountUserId(self) -> str:
        return self.__twitchAccountUserId

    async def getTwitchAnonymousGifterUserId(self) -> str:
        return self.__twitchAnonymousGifterUserId

    async def getValorantUserId(self) -> str:
        return self.__valorantUserId
