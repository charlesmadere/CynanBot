import locale
from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AddQueuedGamesResult:
    amountAdded: int
    newQueueSize: int
    oldQueueSize: int

    @property
    def amountAddedStr(self) -> str:
        return locale.format_string("%d", self.amountAdded, grouping = True)

    @property
    def newQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.newQueueSize, grouping = True)

    @property
    def oldQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.oldQueueSize, grouping = True)
