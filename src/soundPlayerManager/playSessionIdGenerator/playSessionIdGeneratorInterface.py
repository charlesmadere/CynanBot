from abc import ABC, abstractmethod


class PlaySessionIdGeneratorInterface(ABC):

    @abstractmethod
    async def generatePlaySessionId(self) -> str:
        pass
