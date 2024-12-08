from abc import ABC, abstractmethod

from .crowdControlAutomatorData import CrowdControlAutomatorData


class CrowdControlAutomatorInterface(ABC):

    @abstractmethod
    async def applyGameShuffleAutomator(self, automatorData: CrowdControlAutomatorData):
        pass
