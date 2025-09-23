from dataclasses import dataclass

from .absPixelsDiceState import AbsPixelsDiceState


@dataclass(frozen = True)
class PixelsDiceBatteryState(AbsPixelsDiceState):
    isCharging: bool
    battery: int
