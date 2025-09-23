from dataclasses import dataclass

from .absPixelsDiceEvent import AbsPixelsDiceEvent
from ..diceBluetoothInfo import DiceBluetoothInfo


@dataclass(frozen = True)
class PixelsDiceClientDisconnectedEvent(AbsPixelsDiceEvent):
    previouslyConnectedDice: DiceBluetoothInfo | None
