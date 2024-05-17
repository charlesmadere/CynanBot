from dataclasses import dataclass

from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType


@dataclass(frozen = True)
class TtsCheerDonation(TtsDonation):
    bits: int

    @property
    def donationType(self) -> TtsDonationType:
        return TtsDonationType.CHEER
