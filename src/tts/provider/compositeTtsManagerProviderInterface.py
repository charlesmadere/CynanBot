from abc import ABC, abstractmethod

from ..compositeTtsManagerInterface import CompositeTtsManagerInterface


class CompositeTtsManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        pass
