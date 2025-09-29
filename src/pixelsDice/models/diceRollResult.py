import locale

from dataclasses import dataclass


@dataclass(frozen = True)
class DiceRollResult:
    remainingQueueSize: int
    roll: int

    @property
    def remainingQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.remainingQueueSize, grouping = True)
