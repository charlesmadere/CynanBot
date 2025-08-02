import locale

from dataclasses import dataclass


@dataclass(frozen = True)
class CalculatedTimeoutDuration:
    seconds: int
    message: str

    @property
    def secondsStr(self) -> str:
        return locale.format_string("%d", self.seconds, grouping = True)
