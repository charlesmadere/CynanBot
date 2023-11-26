import locale

import misc.utils as utils


class CutenessBoosterPack():

    def __init__(
        self,
        amount: int,
        rewardId: str
    ):
        if not utils.isValidNum(amount):
            raise ValueError(f'amount argument is malformed: \"{amount}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__amount: int = amount
        self.__rewardId: str = rewardId

    def getAmount(self) -> int:
        return self.__amount

    def getAmountStr(self) -> str:
        return locale.format_string("%d", self.__amount, grouping = True)

    def getRewardId(self) -> str:
        return self.__rewardId
