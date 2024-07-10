from .editCheerActionResult import EditCheerActionResult
from ...misc import utils as utils


class NotFoundEditCheerActionResult(EditCheerActionResult):

    def __init__(self, bits: int, twitchChannelId: str):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is malformed: {bits}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__bits: int = bits
        self.__twitchChannelId: str = twitchChannelId

    @property
    def bits(self) -> int:
        return self.__bits

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
