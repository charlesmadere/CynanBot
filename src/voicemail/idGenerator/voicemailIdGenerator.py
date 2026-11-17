from typing import Final

from .voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface
from ...misc.randomUtilsInterface import RandomUtilsInterface


class VoicemailIdGenerator(VoicemailIdGeneratorInterface):

    def __init__(
        self,
        randomUtils: RandomUtilsInterface,
    ):
        if not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')

        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils

    async def generateVoicemailId(self) -> str:
        return self.__randomUtils.uuid()[:3]
