from dataclasses import dataclass

from .absPixelsDiceState import AbsPixelsDiceState


@dataclass(frozen = True)
class PixelsDiceRollState(AbsPixelsDiceState):
    roll: int
