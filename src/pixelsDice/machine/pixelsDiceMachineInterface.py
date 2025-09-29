from abc import ABC, abstractmethod

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.diceRollRequest import DiceRollRequest


class PixelsDiceMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: PixelsDiceEventListener | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitRequest(self, request: DiceRollRequest) -> int:
        pass
