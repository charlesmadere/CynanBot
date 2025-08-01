from abc import ABC, abstractmethod


class ChatterInventoryItemUseMachineInterface(ABC):

    @abstractmethod
    def start(self):
        pass
