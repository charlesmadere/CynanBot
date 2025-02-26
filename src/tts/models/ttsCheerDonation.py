from dataclasses import dataclass

from .ttsDonation import TtsDonation
from .ttsDonationType import TtsDonationType


@dataclass(frozen = True)
class TtsCheerDonation(TtsDonation):
    bits: int

    @property
    def donationType(self) -> TtsDonationType:
        return TtsDonationType.CHEER
