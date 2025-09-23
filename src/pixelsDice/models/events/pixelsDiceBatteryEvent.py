from dataclasses import dataclass

from .absPixelsDiceEvent import AbsPixelsDiceEvent
from ..diceBluetoothInfo import DiceBluetoothInfo


@dataclass(frozen = True)
class PixelsDiceBatteryEvent(AbsPixelsDiceEvent):
    isCharging: bool
    connectedDice: DiceBluetoothInfo
    battery: int
