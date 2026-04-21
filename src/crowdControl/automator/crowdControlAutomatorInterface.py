from abc import ABC, abstractmethod

from .crowdControlAutomatorAddResult import CrowdControlAutomatorAddResult
from .crowdControlAutomatorData import CrowdControlAutomatorData
from .crowdControlAutomatorRemovalResult import CrowdControlAutomatorRemovalResult
from ...misc.startable import Startable


class CrowdControlAutomatorInterface(Startable, ABC):

    @abstractmethod
    async def addGameShuffleAutomator(
        self,
        automatorData: CrowdControlAutomatorData,
    ) -> CrowdControlAutomatorAddResult:
        pass

    @abstractmethod
    async def removeGameShuffleAutomator(
        self,
        twitchChannelId: str,
    ) -> CrowdControlAutomatorRemovalResult:
        pass
