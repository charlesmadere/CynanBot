from abc import ABC, abstractmethod

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener


class PixelsDiceMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: PixelsDiceEventListener | None):
        pass

    @abstractmethod
    def start(self):
        pass
