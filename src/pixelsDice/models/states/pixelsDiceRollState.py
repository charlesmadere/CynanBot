from dataclasses import dataclass

from .absPixelsDiceState import AbsPixelsDiceState


@dataclass(frozen = True, slots = True)
class PixelsDiceRollState(AbsPixelsDiceState):
    rawData: bytearray
    roll: int
