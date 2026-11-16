from typing import Final

from .crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ...misc.randomUtilsInterface import RandomUtilsInterface


class CrowdControlIdGenerator(CrowdControlIdGeneratorInterface):

    def __init__(
        self,
        randomUtils: RandomUtilsInterface,
    ):
        if not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')

        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils

    async def generateActionId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateMessageId(self) -> str:
        return self.__randomUtils.uuid()
