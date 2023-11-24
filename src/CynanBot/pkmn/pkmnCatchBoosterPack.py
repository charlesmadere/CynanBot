from typing import Optional

try:
    from .pkmnCatchType import PkmnCatchType
except:
    from .pkmn.pkmnCatchType import PkmnCatchType

try:
    import CynanBotCommon.utils as utils
except:
    from ...CynanBotCommon.utils import utils


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
