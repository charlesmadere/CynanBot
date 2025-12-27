import locale
from typing import Final

from ..misc import utils as utils


class CutenessEntry:

    def __init__(
        self,
        cuteness: int,
        userId: str,
        userName: str,
    ):
        if not utils.isValidInt(cuteness):
            raise TypeError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif cuteness < 0 or cuteness > utils.getLongMaxSafeSize():
            raise ValueError(f'cuteness argument is out of bounds: {cuteness}')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness: Final[int] = cuteness
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName

    @property
    def cuteness(self) -> int:
        return self.__cuteness

    @property
    def cutenessStr(self) -> str:
        return locale.format_string("%d", self.cuteness, grouping = True)

    @property
    def userId(self) -> str:
        return self.__userId

    @property
    def userName(self) -> str:
        return self.__userName
