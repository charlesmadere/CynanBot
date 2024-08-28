from abc import ABC, abstractmethod


class CrowdControlIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass
