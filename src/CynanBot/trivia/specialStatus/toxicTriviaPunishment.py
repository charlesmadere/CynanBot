import locale

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessResult import CutenessResult


class ToxicTriviaPunishment():

    def __init__(
        self,
        cutenessResult: CutenessResult,
        numberOfPunishments: int,
        punishedByPoints: int,
        userId: str,
        userName: str
    ):
        assert isinstance(cutenessResult, CutenessResult), f"malformed {cutenessResult=}"
        if not utils.isValidInt(numberOfPunishments):
            raise ValueError(f'numberOfPunishments argument is malformed: \"{numberOfPunishments}\"')
        if numberOfPunishments < 1 or numberOfPunishments > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfPunishments argument is malformed: {numberOfPunishments}')
        if not utils.isValidInt(punishedByPoints):
            raise ValueError(f'punishedByPoints argument is malformed: \"{punishedByPoints}\"')
        if punishedByPoints > 0 or punishedByPoints < utils.getIntMinSafeSize():
            raise ValueError(f'punishedByPoints argument is out of bounds: {punishedByPoints}')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cutenessResult: CutenessResult = cutenessResult
        self.__numberOfPunishments: int = numberOfPunishments
        self.__punishedByPoints: int = punishedByPoints
        self.__userId: str = userId
        self.__userName: str = userName

    def getCutenessResult(self) -> CutenessResult:
        return self.__cutenessResult

    def getNumberOfPunishments(self) -> int:
        return self.__numberOfPunishments

    def getNumberOfPunishmentsStr(self) -> str:
        return locale.format_string("%d", self.__numberOfPunishments, grouping = True)

    def getPunishedByPoints(self) -> int:
        return self.__punishedByPoints

    def getPunishedByPointsStr(self) -> str:
        return locale.format_string("%d", self.__punishedByPoints, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
