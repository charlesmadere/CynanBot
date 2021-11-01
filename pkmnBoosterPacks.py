from enum import Enum, auto

import CynanBotCommon.utils as utils


class PkmnCatchType(Enum):

    GREAT = auto()
    NORMAL = auto()
    SHINY_ONLY = auto()
    ULTRA = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'great':
            return PkmnCatchType.GREAT
        elif text == 'normal':
            return PkmnCatchType.NORMAL
        elif text == 'shinyOnly':
            return PkmnCatchType.SHINY_ONLY
        elif text == 'ultra':
            return PkmnCatchType.ULTRA
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{text}\"')

    def getSortOrder(self) -> int:
        if self is PkmnCatchType.GREAT:
            return 1
        elif self is PkmnCatchType.NORMAL:
            return 0
        elif self is PkmnCatchType.SHINY_ONLY:
            return 3
        elif self is PkmnCatchType.ULTRA:
            return 2
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{self}\"')


class PkmnCatchBoosterPack():

    def __init__(
        self,
        pkmnCatchType: PkmnCatchType,
        rewardId: str
    ):
        if pkmnCatchType is None:
            raise ValueError(f'pkmnCatchType argument is malformed: \"{pkmnCatchType}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__pkmnCatchType: PkmnCatchType = pkmnCatchType
        self.__rewardId: str = rewardId

    def getCatchType(self) -> PkmnCatchType:
        return self.__pkmnCatchType

    def getRewardId(self) -> str:
        return self.__rewardId
