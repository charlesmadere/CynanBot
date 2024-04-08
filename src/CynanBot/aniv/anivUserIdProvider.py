import CynanBot.misc.utils as utils
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface


class AnivUserIdProvider(AnivUserIdProviderInterface):

    def __init__(self, anivUserId: str | None = '749050409'):
        if anivUserId is not None and not isinstance(anivUserId, str):
            raise TypeError(f'anivUserId argument is malformed: \"{anivUserId}\"')

        self.__anivUserId: str | None = anivUserId

    async def getAnivUserId(self) -> str | None:
        return self.__anivUserId
