from dataclasses import dataclass

from .absPixelsDiceEvent import AbsPixelsDiceEvent
from ..diceBluetoothInfo import DiceBluetoothInfo


@dataclass(frozen = True)
class PixelsDiceClientConnectedEvent(AbsPixelsDiceEvent):
    connectedDice: DiceBluetoothInfo
