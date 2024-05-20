from dataclasses import dataclass
import locale


@dataclass(frozen = True)
class ClearQueuedGamesResult():
    amountRemoved: int
    oldQueueSize: int

    @property
    def amountRemovedStr(self) -> str:
        return locale.format_string("%d", self.amountRemoved, grouping = True)

    @property
    def oldQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.oldQueueSize, grouping = True)
