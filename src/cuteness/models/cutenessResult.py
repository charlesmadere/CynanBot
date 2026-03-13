import locale
from dataclasses import dataclass

from ..cutenessDate import CutenessDate


@dataclass(frozen = True, slots = True)
class CutenessResult:
    cutenessDate: CutenessDate
    cuteness: int | None
    twitchChannelId: str
    userId: str

    @property
    def cutenessStr(self) -> str:
        cuteness = self.requireCuteness()
        return locale.format_string("%d", cuteness, grouping = True)

    def requireCuteness(self) -> int:
        if self.cuteness is None:
            raise RuntimeError(f'No cuteness value is available ({self=})')

        return self.cuteness
