import CynanBot.misc.utils as utils
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface


class AnivUserIdProvider(AnivUserIdProviderInterface):

    def __init__(self, anivUserId: str = '749050409'):
        if not utils.isValidStr(anivUserId):
            raise ValueError(f'anivUserId argument is malformed: \"{anivUserId}\"')

        self.__anivUserId: str = anivUserId

    async def getAnivUserId(self) -> str:
        return self.__anivUserId
