from dataclasses import dataclass

from .absPixelsDiceEvent import AbsPixelsDiceEvent
from ..diceBluetoothInfo import DiceBluetoothInfo


@dataclass(frozen = True, slots = True)
class PixelsDiceRollEvent(AbsPixelsDiceEvent):
    connectedDice: DiceBluetoothInfo
    roll: int
