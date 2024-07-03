from abc import ABC, abstractmethod


class CheerActionIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass
