import locale

import CynanBot.misc.utils as utils


class AddQueuedGamesResult():

    def __init__(self, amountAdded: int, newQueueSize: int, oldQueueSize: int):
        if not utils.isValidInt(amountAdded):
            raise ValueError(f'amountAdded argument is malformed: \"{amountAdded}\"')
        elif amountAdded < 0 or amountAdded > utils.getIntMaxSafeSize():
            raise ValueError(f'amountAdded argument is out of bounds: {amountAdded}')
        elif not utils.isValidInt(newQueueSize):
            raise ValueError(f'newQueueSize argument is malformed: \"{newQueueSize}\"')
        elif newQueueSize < 0 or newQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'newQueueSize argument is out of bounds: {newQueueSize}')
        elif not utils.isValidInt(oldQueueSize):
            raise ValueError(f'oldQueueSize argument is malformed: \"{oldQueueSize}\"')
        elif oldQueueSize < 0 or oldQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'oldQueueSize argument is out of bounds: {oldQueueSize}')

        self.__amountAdded: int = amountAdded
        self.__newQueueSize: int = newQueueSize
        self.__oldQueueSize: int = oldQueueSize

    def getAmountAdded(self) -> int:
        return self.__amountAdded

    def getAmountAddedStr(self) -> str:
        return locale.format_string("%d", self.__amountAdded, grouping = True)

    def getNewQueueSize(self) -> int:
        return self.__newQueueSize

    def getNewQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__newQueueSize, grouping = True)

    def getOldQueueSize(self) -> int:
        return self.__oldQueueSize

    def getOldQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__oldQueueSize, grouping = True)

    def __str__(self) -> str:
        return f'amountAdded={self.__amountAdded}, newQueueSize={self.__newQueueSize}, oldQueueSize={self.__oldQueueSize}'
