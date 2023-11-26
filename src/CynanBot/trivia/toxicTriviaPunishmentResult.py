import locale
from typing import List

import misc.utils as utils
from trivia.toxicTriviaPunishment import ToxicTriviaPunishment


class ToxicTriviaPunishmentResult():

    def __init__(
        self,
        totalPointsStolen: int,
        toxicTriviaPunishments: List[ToxicTriviaPunishment]
    ):
        if not utils.isValidInt(totalPointsStolen):
            raise ValueError(f'totalPointsStolen argument is malformed: \"{totalPointsStolen}\"')
        elif totalPointsStolen < 1 or totalPointsStolen > utils.getIntMaxSafeSize():
            raise ValueError(f'totalPointsStolen argument is out of bounds: {totalPointsStolen}')
        elif not utils.hasItems(toxicTriviaPunishments):
            raise ValueError(f'toxicTriviaPunishments argument is malformed: \"{toxicTriviaPunishments}\"')

        self.__totalPointsStolen: int = totalPointsStolen
        self.__toxicTriviaPunishments: List[ToxicTriviaPunishment] = toxicTriviaPunishments

    def getNumberOfToxicTriviaPunishments(self) -> int:
        return len(self.__toxicTriviaPunishments)

    def getTotalPointsStolen(self) -> int:
        return self.__totalPointsStolen

    def getTotalPointsStolenStr(self) -> str:
        return locale.format_string("%d", self.__totalPointsStolen, grouping = True)

    def getToxicTriviaPunishments(self) -> List[ToxicTriviaPunishment]:
        return self.__toxicTriviaPunishments
