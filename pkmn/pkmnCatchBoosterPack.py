from pkmn.pkmnCatchType import PkmnCatchType

try:
    import CynanBotCommon.utils as utils
except:
    from .CynanBotCommon.utils import utils


class PkmnCatchBoosterPack():

    def __init__(
        self,
        pkmnCatchType: PkmnCatchType,
        rewardId: str
    ):
        if not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__pkmnCatchType: PkmnCatchType = pkmnCatchType
        self.__rewardId: str = rewardId

    def getCatchType(self) -> PkmnCatchType:
        return self.__pkmnCatchType

    def getRewardId(self) -> str:
        return self.__rewardId

    def hasCatchType(self) -> bool:
        return self.__pkmnCatchType is not None
