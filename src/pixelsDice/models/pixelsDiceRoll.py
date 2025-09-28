from dataclasses import dataclass


@dataclass(frozen = True)
class PixelsDiceRoll:
    roll: int
