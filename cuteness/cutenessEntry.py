import locale

import CynanBotCommon.utils as utils


class CutenessEntry():

    def __init__(
        self,
        cuteness: int,
        userId: str,
        userName: str
    ):
        if not utils.isValidNum(cuteness):
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness: int = cuteness
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> int:
        return self.__cuteness

    def getCutenessStr(self) -> str:
        return locale.format_string("%d", self.__cuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def toStr(self) -> str:
        return f'{self.__userName} ({self.getCutenessStr()})'
