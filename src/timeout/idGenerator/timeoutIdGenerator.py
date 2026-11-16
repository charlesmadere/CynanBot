from typing import Final

from .timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...misc.randomUtilsInterface import RandomUtilsInterface


class TimeoutIdGenerator(TimeoutIdGeneratorInterface):

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
