from abc import ABC, abstractmethod


class TimeoutActionIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass
