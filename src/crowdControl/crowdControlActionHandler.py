from abc import ABC, abstractmethod

from .actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from .actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from .crowdControlActionHandleResult import CrowdControlActionHandleResult


class CrowdControlActionHandler(ABC):

    @abstractmethod
    async def handleButtonPressAction(
        self,
        action: ButtonPressCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        pass

    @abstractmethod
    async def handleGameShuffleAction(
        self,
        action: GameShuffleCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        pass
