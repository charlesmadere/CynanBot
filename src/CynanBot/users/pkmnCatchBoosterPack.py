from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.users.pkmnCatchType import PkmnCatchType


class PkmnCatchBoosterPack():

    def __init__(
        self,
        pkmnCatchType: Optional[PkmnCatchType],
        rewardId: str
    ):
        assert pkmnCatchType is None or isinstance(pkmnCatchType, PkmnCatchType), f"malformed {pkmnCatchType=}"
        if not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__pkmnCatchType: Optional[PkmnCatchType] = pkmnCatchType
        self.__rewardId: str = rewardId

    def getCatchType(self) -> Optional[PkmnCatchType]:
        return self.__pkmnCatchType

    def getRewardId(self) -> str:
        return self.__rewardId

    def hasCatchType(self) -> bool:
        return self.__pkmnCatchType is not None
