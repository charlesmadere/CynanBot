import locale
from dataclasses import dataclass

from .ttsDonation import TtsDonation


@dataclass(frozen = True, slots = True)
class TtsCheerDonation(TtsDonation):
    bits: int

    @property
    def bitsStr(self) -> str:
        return locale.format_string("%d", self.bits, grouping = True)
