import locale
from dataclasses import dataclass
from typing import Any

from .cheerActionBitRequirement import CheerActionBitRequirement
from .cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc import utils as utils


@dataclass(frozen = True)
class CheerAction():
    bitRequirement: CheerActionBitRequirement
    streamStatusRequirement: CheerActionStreamStatusRequirement
    actionType: CheerActionType
    amount: int
    durationSeconds: int | None
    actionId: str
    tag: str | None
    userId: str
    userName: str

    @property
    def amountStr(self) -> str:
        return locale.format_string("%d", self.amount, grouping = True)

    @property
    def durationSecondsStr(self) -> str:
        durationSeconds = self.requireDurationSeconds()
        return locale.format_string("%d", durationSeconds, grouping = True)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CheerAction):
            return False

        return self.actionId == other.actionId and self.userId == other.userId

    def __hash__(self) -> int:
        return hash((self.actionId, self.userId))

    def requireDurationSeconds(self) -> int:
        if not utils.isValidInt(self.durationSeconds):
            raise RuntimeError(f'No durationSeconds value is available: {self}')

        return self.durationSeconds
