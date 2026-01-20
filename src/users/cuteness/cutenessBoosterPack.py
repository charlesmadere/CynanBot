import locale
from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CutenessBoosterPack:
    amount: int
    rewardId: str

    @property
    def amountStr(self) -> str:
        return locale.format_string("%d", self.amount, grouping = True)
