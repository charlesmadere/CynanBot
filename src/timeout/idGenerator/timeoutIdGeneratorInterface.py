from abc import ABC, abstractmethod


class TimeoutIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass

    @abstractmethod
    async def generateEventId(self) -> str:
        pass
