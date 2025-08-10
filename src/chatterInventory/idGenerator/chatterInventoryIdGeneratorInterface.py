from abc import ABC, abstractmethod


class ChatterInventoryIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass

    @abstractmethod
    async def generateEventId(self) -> str:
        pass

    @abstractmethod
    async def generateRequestId(self) -> str:
        pass
