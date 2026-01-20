import locale

from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AnivTimeoutData:
    randomNumber: float
    timeoutScale: float | None
    timeoutProbability: float
    durationSeconds: int
    durationMessage: str

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)
