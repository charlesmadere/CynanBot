import locale

from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CalculatedTimeoutDuration:
    seconds: int
    message: str
    shorthandMessage: str

    @property
    def secondsStr(self) -> str:
        return locale.format_string("%d", self.seconds, grouping = True)
