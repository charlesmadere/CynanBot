import locale
from dataclasses import dataclass


@dataclass(frozen = True)
class CutenessEntry():
    cuteness: int
    userId: str
    userName: str

    @property
    def cutenessStr(self) -> str:
        return locale.format_string("%d", self.cuteness, grouping = True)
