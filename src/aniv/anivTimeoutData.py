import locale

from dataclasses import dataclass


@dataclass(frozen = True)
class AnivTimeoutData:
    randomNumber: float
    timeoutProbability: float
    durationSeconds: int

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)
