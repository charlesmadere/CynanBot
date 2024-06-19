import locale
from dataclasses import dataclass
from typing import Any

from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType


@dataclass(frozen = True)
class CheerAction():
    bitRequirement: CheerActionBitRequirement
    streamStatusRequirement: CheerActionStreamStatusRequirement
    actionType: CheerActionType
    amount: int
    durationSeconds: int
    actionId: str
    userId: str
    userName: str

    @property
    def amountStr(self) -> str:
        return locale.format_string("%d", self.amount, grouping = True)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CheerAction):
            return False

        return self.actionId == other.actionId and self.userId == other.userId

    def __hash__(self) -> int:
        return hash((self.actionId, self.userId))
