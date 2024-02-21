import locale
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessDate import CutenessDate


class CutenessResult():

    def __init__(
        self,
        cutenessDate: CutenessDate,
        cuteness: Optional[int],
        userId: str,
        userName: str
    ):
        assert isinstance(cutenessDate, CutenessDate), f"malformed {cutenessDate=}"
        if cuteness is not None and not utils.isValidInt(cuteness):
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        if cuteness is not None and (cuteness < 0 or cuteness > utils.getLongMaxSafeSize()):
            raise ValueError(f'cuteness argument is out of bounds: {cuteness}')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__cuteness: Optional[int] = cuteness
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> Optional[int]:
        return self.__cuteness

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getCutenessStr(self) -> str:
        cuteness = self.requireCuteness()
        return locale.format_string("%d", cuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def requireCuteness(self) -> int:
        cuteness = self.__cuteness

        if not utils.isValidInt(cuteness):
            raise RuntimeError(f'No cuteness value is available: {cuteness}')

        return cuteness
