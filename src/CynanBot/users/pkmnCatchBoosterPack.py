from typing import Optional

import misc.utils as utils
from users.pkmnCatchType import PkmnCatchType


class PkmnCatchBoosterPack():

    def __init__(
        self,
        pkmnCatchType: Optional[PkmnCatchType],
        rewardId: str
    ):
        if pkmnCatchType is not None and not isinstance(pkmnCatchType, PkmnCatchType):
            raise ValueError(f'pkmnCatchType argument is malformed: \"{pkmnCatchType}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__pkmnCatchType: Optional[PkmnCatchType] = pkmnCatchType
        self.__rewardId: str = rewardId

    def getCatchType(self) -> Optional[PkmnCatchType]:
        return self.__pkmnCatchType

    def getRewardId(self) -> str:
        return self.__rewardId

    def hasCatchType(self) -> bool:
        return self.__pkmnCatchType is not None
