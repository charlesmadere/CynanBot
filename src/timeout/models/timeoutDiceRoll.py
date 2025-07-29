from dataclasses import dataclass


@dataclass(frozen = True)
class TimeoutDiceRoll:
    dieSize: int
    roll: int
