from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType


class TtsCheerDonation(TtsDonation):

    def __init__(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits: int = bits

    def getBits(self) -> int:
        return self.__bits

    def getType(self) -> TtsDonationType:
        return TtsDonationType.CHEER

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'type': self.getType()
        }
