from abc import ABC, abstractmethod

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.diceRollRequest import DiceRollRequest
from ...misc.startable import Startable


class PixelsDiceMachineInterface(Startable, ABC):

    @property
    @abstractmethod
    def isConnected(self) -> bool:
        pass

    @abstractmethod
    def setEventListener(self, listener: PixelsDiceEventListener | None):
        pass

    @abstractmethod
    def submitRequest(self, request: DiceRollRequest) -> int:
        pass
