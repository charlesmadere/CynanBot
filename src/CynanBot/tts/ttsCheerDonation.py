from typing import Any, Dict

import misc.utils as utils
from tts.ttsDonation import TtsDonation
from tts.ttsDonationType import TtsDonationType


class TtsCheerDonation(TtsDonation):

    def __init__(self, bits: int):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits: int = bits

    def getBits(self) -> int:
        return self.__bits

    def getType(self) -> TtsDonationType:
        return TtsDonationType.CHEER

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'bits': self.__bits,
            'type': self.getType()
        }
