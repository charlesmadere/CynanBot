import CynanBot.misc.utils as utils
from CynanBot.users.pkmnCatchType import PkmnCatchType


class PkmnCatchBoosterPack():

    def __init__(
        self,
        pkmnCatchType: PkmnCatchType | None,
        rewardId: str
    ):
        if pkmnCatchType is not None and not isinstance(pkmnCatchType, PkmnCatchType):
            raise TypeError(f'pkmnCatchType argument is malformed: \"{pkmnCatchType}\"')
        elif not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__pkmnCatchType: PkmnCatchType | None = pkmnCatchType
        self.__rewardId: str = rewardId

    def getCatchType(self) -> PkmnCatchType | None:
        return self.__pkmnCatchType

    def getRewardId(self) -> str:
        return self.__rewardId

    def hasCatchType(self) -> bool:
        return self.__pkmnCatchType is not None
