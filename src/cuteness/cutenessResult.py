import locale
from dataclasses import dataclass

from .cutenessDate import CutenessDate
from ..misc import utils as utils


@dataclass(frozen = True, slots = True)
class CutenessResult:
    cutenessDate: CutenessDate
    cuteness: int | None
    userId: str
    userName: str

    @property
    def cutenessStr(self) -> str:
        cuteness = self.requireCuteness()
        return locale.format_string("%d", cuteness, grouping = True)

    def requireCuteness(self) -> int:
        if not utils.isValidInt(self.cuteness):
            raise RuntimeError(f'No cuteness value is available: {self}')

        return self.cuteness
