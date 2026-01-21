from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TimeoutDiceRoll:
    dieSize: int
    roll: int
