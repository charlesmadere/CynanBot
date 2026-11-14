from typing import Final

from .chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ...misc.randomUtilsInterface import RandomUtilsInterface


class ChatterInventoryIdGenerator(ChatterInventoryIdGeneratorInterface):

    def __init__(
        self,
        randomUtils: RandomUtilsInterface,
    ):
        if not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')

        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils

    async def generateActionId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateEventId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateRequestId(self) -> str:
        return self.__randomUtils.uuid()
