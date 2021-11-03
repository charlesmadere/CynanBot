import CynanBotCommon.utils as utils

from pkmn.pkmnCatchType import PkmnCatchType


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
