from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterUser:
    characterAllowance: int
    characterUsage: int
    currentPlan: str | None
    status: str
