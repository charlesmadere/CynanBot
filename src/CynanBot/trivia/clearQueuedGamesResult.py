import locale

import misc.utils as utils


class ClearQueuedGamesResult():

    def __init__(self, amountRemoved: int, oldQueueSize: int):
        if not utils.isValidInt(amountRemoved):
            raise ValueError(f'amountRemoved argument is malformed: \"{amountRemoved}\"')
        elif amountRemoved < 0 or amountRemoved > utils.getIntMaxSafeSize():
            raise ValueError(f'amountRemoved argument is out of bounds: {amountRemoved}')
        elif not utils.isValidInt(oldQueueSize):
            raise ValueError(f'oldQueueSize argument is malformed: \"{oldQueueSize}\"')
        elif oldQueueSize < 0 or oldQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'oldQueueSize argument is out of bounds: {oldQueueSize}')

        self.__amountRemoved: int = amountRemoved
        self.__oldQueueSize: int = oldQueueSize

    def getAmountRemoved(self) -> int:
        return self.__amountRemoved

    def getAmountRemovedStr(self) -> str:
        return locale.format_string("%d", self.__amountRemoved, grouping = True)

    def getOldQueueSize(self) -> int:
        return self.__oldQueueSize

    def getOldQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__oldQueueSize, grouping = True)

    def toStr(self) -> str:
        return f'amountRemoved={self.__amountRemoved}, oldQueueSize={self.__oldQueueSize}'
